from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Interest, Experience
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import InterestSerializer, ExperienceSerializer


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def interest_list(request):
    if request.method in ("GET", "HEAD"):
        interests = (
            Interest.objects
            .prefetch_related("starred_by")
            .order_by("id")
        )

        name = request.query_params.get("name", "").strip()

        if name:
            interests = interests.filter(name__icontains=name)

        serializer = InterestSerializer(
            interests,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)

    serializer = InterestSerializer(
        data=request.data,
        context={"request": request},
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def interest_detail(request, interest_id):
    interest = get_object_or_404(
        Interest.objects.prefetch_related("starred_by"),
        pk=interest_id,
    )

    if request.method in ("GET", "HEAD"):
        serializer = InterestSerializer(
            interest,
            context={"request": request},
        )

        return Response(serializer.data)

    if request.method == "DELETE":
        interest.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    serializer = InterestSerializer(
        interest,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def interest_star(request, interest_id):
    interest = get_object_or_404(
        Interest,
        pk=interest_id,
    )

    if interest.starred_by.filter(pk=request.user.pk).exists():
        interest.starred_by.remove(request.user)
    else:
        interest.starred_by.add(request.user)

    serializer = InterestSerializer(
        interest,
        context={"request": request},
    )

    return Response(serializer.data)

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list(request):
    if request.method in ("GET", "HEAD"):
        experiences = (
            Experience.objects
            .prefetch_related("starred_by")
            .order_by("-started_at")
        )

        title = request.query_params.get("title", "").strip()

        if title:
            experiences = experiences.filter(
                title__icontains=title
            )

        serializer = ExperienceSerializer(
            experiences,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)

    serializer = ExperienceSerializer(
        data=request.data,
        context={"request": request},
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"),
        pk=experience_id,
    )

    if request.method in ("GET", "HEAD"):
        serializer = ExperienceSerializer(
            experience,
            context={"request": request},
        )

        return Response(serializer.data)

    if request.method == "DELETE":
        experience.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    serializer = ExperienceSerializer(
        experience,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    experience = get_object_or_404(
        Experience,
        pk=experience_id,
    )

    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)

    serializer = ExperienceSerializer(
        experience,
        context={"request": request},
    )

    return Response(serializer.data)