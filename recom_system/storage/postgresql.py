from recom_system.app.models import Anomaly, PowerComponent, UserProfile


class PostgresStorage:
    @staticmethod
    def create_anomaly(anomaly_id, description, severity, timestamp,
                       recommended_product, user):
        anomaly = Anomaly.objects.create(
            anomaly_id=anomaly_id,
            description=description,
            severity=severity,
            timestamp=timestamp,
            recommended_product=recommended_product
        )
        anomaly.user_names.set([user])
        return anomaly

    @staticmethod
    def reset_anomaly_db():
        Anomaly.objects.all().delete()  # Clear anomalies
        UserProfile.objects.all().delete()  # Clear user profiles
        PowerComponent.objects.all().delete()  # Clear power components

    @staticmethod
    def get_all_anomalies():
        return Anomaly.objects.all()

    @staticmethod
    def get_all_user_profiles():
        return UserProfile.objects.all()

    @staticmethod
    def get_all_power_components():
        return PowerComponent.objects.all()

    @staticmethod
    def get_anomaly(anomaly_id):
        try:
            return Anomaly.objects.get(anomaly_id=anomaly_id)
        except Anomaly.DoesNotExist:
            return

    @staticmethod
    def create_user(user_name, role, email):
        return UserProfile.objects.create(
            user_name=user_name,
            role=role,
            email=email
        )

    @staticmethod
    def create_component(component_id, name, location, status, component_type,
                         anomaly):
        component = PowerComponent.objects.create(
            component_id=component_id,
            name=name,
            location=location,
            status=status,
            component_type=component_type
        )
        component.anomalies.add(anomaly)
        return component

    @staticmethod
    def get_component_from_anomaly(anomaly):
        return PowerComponent.objects.filter(anomalies=anomaly)
