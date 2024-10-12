from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Assignment, Admin,User
from .serializers import AssignmentSerializer, AdminSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

# API for Student Registration 
@api_view(['POST'])
def student_register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)  # Create a token for the user
        return Response({'message': 'User registered successfully!', 'user_id': user.id,'token': token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API for Student Login
@api_view(['POST'])
def student_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    # Authenticate the user
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        if Admin.objects.filter(user=user).exists():
            return Response({"message": "Only students are allowed to login."}, status=status.HTTP_403_FORBIDDEN)
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message': 'Login successful!','token': token.key}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# API for uploading assignments
@api_view(['POST'])
def upload_assignment(request):
    #Checking if currently logged in user is admin
    if Admin.objects.filter(user=request.user).exists():
        return Response({'error': 'Admins are not allowed to upload assignments.'}, status=status.HTTP_403_FORBIDDEN)
         
    serializer = AssignmentSerializer(data=request.data)
    if serializer.is_valid():
        assignment = serializer.save(user=request.user) # Assuming authenticated user
        assignment.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API to retrieve all Admins
@api_view(['GET'])
def all_admins(request):
    admins = Admin.objects.all()
    serializer = AdminSerializer(admins, many=True)
    return Response(serializer.data)

# API for Admin Registration
@api_view(['POST'])
def admin_register(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Create Admin Profile for this user
        department = request.data.get('department')  # Get the department from request data
        if department:
           admin= Admin.objects.create(user=user, department=department)
        else:
            return Response({'error': 'Department is required for admin registration'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({'message': 'Admin registered successfully!', 'admin_id': admin.id, 'token': token.key}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API for Admin Login
@api_view(['POST'])
def admin_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Authenticate the user
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Check if the user has an AdminProfile (i.e., is an admin)
        try:
            admin_profile = Admin.objects.get(user=user)
        except Admin.DoesNotExist:
            return Response({'error': 'User is not an admin'}, status=status.HTTP_403_FORBIDDEN)
        
        # Generate or get the token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({'message': 'Admin logged in successfully!', 'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
  

# API to list assignments for a particular admin
@api_view(['GET'])
def assignment_show(request):
    try:
        # Admin Profile linked to ogged-in user
        admin_profile = Admin.objects.get(user=request.user)
        
        # Now getting assignments according to admin
        assignments = Assignment.objects.filter(admin=admin_profile)
        
        # Create a list ot hold assignments
        assignments_data=[]

        for assignment in assignments:
            data={
                'user':assignment.user.username,
                'task':assignment.task,
                'submittedAt':assignment.submittedAt,
            }
            assignments_data.append(data)
        return Response({'assignments': assignments_data}, status=status.HTTP_200_OK)
    
    except Admin.DoesNotExist:
        return Response({'error': 'Admin profile not found for the user'}, status=status.HTTP_403_FORBIDDEN)

# API to accept an assignment
@api_view(['PATCH'])
def assignment_accept(request, id):
    try:
        # Check if the user is an admin
        admin_profile = Admin.objects.filter(user=request.user).first()
        if not admin_profile:
            return Response({'error': 'Only admins can accept assignments.'}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve the assignment and ensure it is tagged to the admin
        assignment = get_object_or_404(Assignment, id=id, admin=admin_profile)

        # Update the assignment status to 'Accepted'
        assignment.status = 'Accepted'
        assignment.save()
        return Response({"message": "Assignment Accepted"}, status=status.HTTP_200_OK)
    except Assignment.DoesNotExist:
        return Response({'error': 'Assignment not found or you are not authorized to accept this assignment.'}, status=status.HTTP_404_NOT_FOUND)

# API to reject an assignment
@api_view(['PATCH'])
def assignment_reject(request, id):
    try:
        # Check if the user is an admin
        admin_profile = Admin.objects.filter(user=request.user).first()
        if not admin_profile:
            return Response({'error': 'Only admins can accept assignments.'}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve the assignment and ensure it is tagged to the admin
        assignment = get_object_or_404(Assignment, id=id, admin=admin_profile)

        # Update the assignment status to 'Rejected'
        assignment.status = 'Rejected'
        assignment.save()
        return Response({"message": "Assignment Rejected"}, status=status.HTTP_200_OK)
    except Assignment.DoesNotExist:
        return Response({'error': 'Assignment not found or you are not authorized to reject this assignment.'}, status=status.HTTP_404_NOT_FOUND)