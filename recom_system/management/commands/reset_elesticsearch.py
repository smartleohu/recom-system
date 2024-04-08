from django.core.management.commands.runserver import \
    Command as RunserverCommand

from recom_system.storage.elasticsearch import ElasticSearchStorage


class Command(RunserverCommand):
    help = "Clear all docs in ElasticSearch"

    def handle(self, *args, **options):
        ElasticSearchStorage.get_instance().clear()
