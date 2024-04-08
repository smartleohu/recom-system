import pytest

from recom_system.app.models import Anomaly, PowerComponent, UserProfile


@pytest.fixture(autouse=True)
def reset_anomaly_db():
    Anomaly.objects.all().delete()  # Clear anomalies
    UserProfile.objects.all().delete()  # Clear user profiles
    PowerComponent.objects.all().delete()  # Clear power components


def test_user_profile_creation():
    user_profile = UserProfile.objects.create(
        user_name='test_user',
        role='Admin',
        email='test@example.com'
    )
    assert user_profile.user_name == 'test_user'
    assert user_profile.role == 'Admin'
    assert user_profile.email == 'test@example.com'


@pytest.mark.django_db
def test_anomaly_creation():
    user_profile = UserProfile.objects.create(
        user_name='test_user',
        role='Admin',
        email='test@example.com'
    )
    anomaly = Anomaly.objects.create(
        anomaly_id='01',
        description='Test anomaly',
        severity='High',
        recommended_product='Product A'
    )
    anomaly.user_names.add(user_profile)
    assert anomaly.anomaly_id == '01'
    assert anomaly.description == 'Test anomaly'
    assert anomaly.severity == 'High'
    assert anomaly.recommended_product == 'Product A'
    assert user_profile in anomaly.user_names.all()


@pytest.mark.django_db
def test_power_component_creation():
    anomaly = Anomaly.objects.create(
        anomaly_id='01',
        description='Test anomaly',
        severity='High',
        recommended_product='Product A'
    )
    power_component = PowerComponent.objects.create(
        component_id='01',
        name='Component A',
        location='Location A',
        status='Active',
        component_type='Type A'
    )
    power_component.anomalies.add(anomaly)
    assert power_component.component_id == '01'
    assert power_component.name == 'Component A'
    assert power_component.location == 'Location A'
    assert power_component.status == 'Active'
    assert power_component.component_type == 'Type A'
    assert anomaly in power_component.anomalies.all()
