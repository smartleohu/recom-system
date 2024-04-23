import logging
import random
import time

logger = logging.getLogger(__name__)


def find_similar_anomalies(anomaly_id):
    # simulate the processing time between 20 and 30 seconds randomly
    proc_time = random.uniform(20, 30)
    # simulate the anomaly_ids and similarities randomly
    anomaly_ids = random.sample(['A1', 'A2', 'A3'], 2)
    similarities = random.sample([
        random.uniform(0.9, 1.0),
        random.uniform(0.8, 0.9),
        random.uniform(0.7, 0.8),
    ], 2)
    logger.info(f'process anomaly_id in question: {anomaly_id} waiting for '
                f'{proc_time}s...')
    time.sleep(proc_time)
    similar_anomalies = [{
        'anomaly_id': a_id,
        'similarity': s_score,
    } for a_id, s_score in zip(anomaly_ids, similarities)]

    return similar_anomalies
