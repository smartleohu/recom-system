from datetime import datetime, timezone

from django.core.management.base import BaseCommand

from recom_system.storage.postgresql import PostgresStorage


class Command(BaseCommand):
    help = 'Clear and initialize some initial data for all models'

    def handle(self, *args, **options):
        # Clear existing data for all models
        PostgresStorage.reset_anomaly_db()

        # Initialize new data for all models
        user1 = PostgresStorage.create_user(user_name='user1', role='Admin',
                                            email='admin@example.com')
        user2 = PostgresStorage.create_user(user_name='user2', role='User',
                                            email='user1@example.com')
        user3 = PostgresStorage.create_user(user_name='user3', role='User',
                                            email='user2@example.com')

        anomaly1 = PostgresStorage.create_anomaly(
            anomaly_id='A1',
            description='Perte de puissance',
            severity='High',
            timestamp=datetime(2023, 1, 1, tzinfo=timezone.utc),
            recommended_product='Product A',
            user=user1
        )
        anomaly2 = PostgresStorage.create_anomaly(
            anomaly_id='A2',
            description='Température élevée',
            severity='Medium',
            timestamp=datetime(2023, 1, 1, tzinfo=timezone.utc),
            recommended_product='Product B',
            user=user2
        )
        anomaly3 = PostgresStorage.create_anomaly(
            anomaly_id='A3',
            description='Fuite de fluide',
            severity='Low',
            timestamp=datetime(2023, 1, 1, tzinfo=timezone.utc),
            recommended_product='Product C',
            user=user3
        )

        component1 = PostgresStorage.create_component(
            component_id='C1',
            name='Turbine 1',
            location='Salle des turbines',
            status='Opérationnel',
            component_type='Turbine',
            anomaly=anomaly1
        )
        component2 = PostgresStorage.create_component(
            component_id='C2',
            name='Réacteur 2',
            location='Salle des réacteurs',
            status='En panne',
            component_type='Réacteur',
            anomaly=anomaly2
        )
        component3 = PostgresStorage.create_component(
            component_id='C3',
            name='Transformateur 3',
            location='Salle des transformateurs',
            status='En attente',
            component_type='Transformateur',
            anomaly=anomaly3
        )

        # Construct the message with record content
        message = "Successfully initialized initial data for all models:\n"
        message += "\n".join(
            [f"user_name: {u.user_name}, Role: {u.role}, Email: {u.email}"
             for u in [user1, user2, user3]]
        )
        message += '\n'
        message += "\n".join([
            f"""Anomaly ID: {a.anomaly_id},
            Description: {a.description},
            Components: {[
                c.name
                for c in PostgresStorage.get_component_from_anomaly(a)
            ]},
            Severity: {a.severity},
            Timestamp: {a.timestamp},
            Users: {[user.user_name for user in a.user_names.all()]},
            Recommended Product: {a.recommended_product}"""
            for a in [anomaly1, anomaly2, anomaly3]]
        )
        message += '\n'
        message += "\n".join([
            f"""Component ID: {c.component_id}, Name: {c.name}, 
            Location: {c.location},
            Status: {c.status}, Type: {c.component_type}"""
            for c in
            [component1, component2, component3]]
        )
        self.stdout.write(self.style.SUCCESS(message))
