from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer


def getNotesList(request):
    notes = Note.objects.all().order_by('-updated')
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


def getNoteDetail(request, pk):
    notes = Note.objects.get(id=pk)
    serializer = NoteSerializer(notes, many=False)
    return Response(serializer.data)


def createNote(request):
    data = request.data
    note = Note.objects.create(
        body=data['body']
    )
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)

def updateNote(request, pk):
    data = request.data
    note = Note.objects.get(id=pk)
    serializer = NoteSerializer(instance=note, data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=400)


def deleteNote(request, pk):
    try:
        note = Note.objects.get(id=pk)
        note.delete()
        return Response({'message': 'Note was deleted!'}, status=204)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=404)