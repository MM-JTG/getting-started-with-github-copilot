from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


def test_get_activities_returns_activity_and_participant_data(
    client: TestClient,
) -> None:
    # Arrange
    expected_fields = {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities

    for activity in activities.values():
        assert expected_fields <= activity.keys()
        assert isinstance(activity["participants"], list)
