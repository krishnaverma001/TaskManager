from django.db.models import F
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.serializers import TaskSerializer
from api.models import Task

@api_view(['GET'])
def task_list(request):
    try:
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            "error": "Unable to fetch tasks",
            "type": "ServerError",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def task_create(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({
        "error": "Invalid input",
        "type": "ValidationError",
        "details": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def task_delete(request, k):
    try:
        task = Task.objects.get(id=k)
        task.delete()
        return Response({'message': 'Task deleted'}, status=status.HTTP_204_NO_CONTENT)

    except Task.DoesNotExist:
        return Response({
            "error": "Task not found",
            "type": "NotFoundError",
            "details": None
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "error": "Server error during delete",
            "type": "ServerError",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def task_toggle(request, k):
    try:
        updated = Task.objects.filter(id=k).update(complete=~F('complete'))
        if not updated:
            raise Task.DoesNotExist
        new_val = Task.objects.get(id=k).complete
        return Response({'id': k, 'complete': new_val})

    except Task.DoesNotExist:
        return Response({
            "error": "Task not found",
            "type": "NotFoundError",
            "details": None
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "error": "Server error during toggle",
            "type": "ServerError",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def task_update(request, k):
    try:
        try:
            task = Task.objects.get(id=k)
        except Task.DoesNotExist:
            return Response({
                "error": "Task not found",
                "type": "NotFoundError",
                "details": None
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({
            "error": "Invalid data",
            "type": "ValidationError",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            "error": "Server error during update",
            "type": "ServerError",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
