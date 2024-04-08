from datetime import datetime

import pytest

from recom_system.app.models import Anomaly, PowerComponent, UserProfile
from recom_system.storage.postgresql import PostgresStorage


@pytest.fixture(autouse=True)
def reset_anomaly_db():
    Anomaly.objects.all().delete()  # Clear anomalies
    UserProfile.objects.all().delete()  # Clear user profiles
    PowerComponent.objects.all().delete()  # Clear power components


@pytest.fixture
def sample_user():
    return UserProfile.objects.create(
        user_name='test_user',
        role='Admin',
        email='test@example.com'
    )


@pytest.fixture
def sample_anomaly(sample_user):
    return PostgresStorage.create_anomaly(
        anomaly_id='test_anomaly',
        description='Test anomaly',
        severity='High',
        timestamp=datetime.now(),
        recommended_product='Product A',
        user=sample_user
    )


@pytest.mark.django_db
def test_create_anomaly(sample_user):
    anomaly = PostgresStorage.create_anomaly(
        anomaly_id='test_anomaly',
        description='Test anomaly',
        severity='High',
        timestamp=datetime.now(),
        recommended_product='Product A',
        user=sample_user
    )
    print(anomaly)
    assert Anomaly.objects.filter(anomaly_id='test_anomaly').exists()


@pytest.mark.django_db
def test_reset_anomaly_db(sample_anomaly):
    PostgresStorage.reset_anomaly_db()
    assert Anomaly.objects.count() == 0
    assert UserProfile.objects.count() == 0
    assert PowerComponent.objects.count() == 0


@pytest.mark.django_db
def test_get_all_anomalies(sample_anomaly):
    anomalies = PostgresStorage.get_all_anomalies()
    assert sample_anomaly in anomalies


@pytest.mark.django_db
def test_get_all_user_profiles(sample_user):
    user_profiles = PostgresStorage.get_all_user_profiles()
    assert sample_user in user_profiles


@pytest.mark.django_db
def test_get_all_power_components(sample_anomaly):
    component = PostgresStorage.create_component(
        component_id='test_component',
        name='Component A',
        location='Location A',
        status='Active',
        component_type='Type A',
        anomaly=sample_anomaly
    )
    components = PostgresStorage.get_all_power_components()
    assert component in components


@pytest.mark.django_db
def test_get_anomaly(sample_anomaly):
    anomaly = PostgresStorage.get_anomaly('test_anomaly')
    assert anomaly == sample_anomaly


@pytest.mark.django_db
def test_create_user():
    user = PostgresStorage.create_user(
        user_name='test_user',
        role='Admin',
        email='test@example.com'
    )
    print(user)
    assert UserProfile.objects.filter(user_name='test_user').exists()


@pytest.mark.django_db
def test_create_component(sample_anomaly):
    component = PostgresStorage.create_component(
        component_id='test_component',
        name='Component A',
        location='Location A',
        status='Active',
        component_type='Type A',
        anomaly=sample_anomaly
    )
    print(component)
    assert PowerComponent.objects.filter(
        component_id='test_component').exists()


@pytest.mark.django_db
def test_get_component_from_anomaly(sample_anomaly):
    component = PostgresStorage.create_component(
        component_id='test_component',
        name='Component A',
        location='Location A',
        status='Active',
        component_type='Type A',
        anomaly=sample_anomaly
    )
    components = PostgresStorage.get_component_from_anomaly(sample_anomaly)
    assert component in components
