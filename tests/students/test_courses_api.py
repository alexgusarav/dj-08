# def test_example():
#     assert False, "Just test example"

import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from random import randint
from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_courses(client, courses_factory):
    courses = courses_factory(_quantity=10)
    response = client.get(f"/api/v1/courses/{courses[0].id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == courses[0].name


@pytest.mark.django_db
def test_get_course_list(client, courses_factory):
    courses = courses_factory(_quantity=10)
    response = client.get("/api/v1/courses/")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_filter_by_id(client, courses_factory):
    courses = courses_factory(_quantity=10)
    random_id = [i.id for i in courses][randint(0, 9)]
    response = client.get(f"/api/v1/courses/?id={random_id}")
    data = response.json()
    assert response.status_code == 200
    assert data[0]["id"] == random_id


@pytest.mark.django_db
def test_filter_by_name(client, courses_factory):
    courses = courses_factory(_quantity=10)
    random_name = [i.name for i in courses][randint(0, 9)]
    response = client.get(f"/api/v1/courses/?name={random_name}")
    data = response.json()
    assert response.status_code == 200
    assert data[0]["name"] == random_name


@pytest.mark.django_db
def test_create_course(client):
    response = client.post(
        path="/api/v1/courses/",
        data={"name": "TESTCOURSE", "students": []}
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_course(client, courses_factory):
    courses = courses_factory(_quantity=10)
    random_id = [i.id for i in courses][randint(0, 9)]
    response = client.patch(
        path=f"/api/v1/courses/{random_id}/",
        data={"name": "TESTCOURSE", "students": []}
    )
    assert response.status_code == 200
    new_response = client.get(f"/api/v1/courses/{random_id}/")
    assert new_response.json()["name"] == "TESTCOURSE"


@pytest.mark.django_db
def test_delete_course(client, courses_factory):
    courses = courses_factory(_quantity=10)
    random_id = [i.id for i in courses][randint(0, 9)]
    response = client.delete(f"/api/v1/courses/{random_id}/")
    assert response.status_code == 204
