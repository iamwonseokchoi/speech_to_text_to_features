import pytest
import pandas as pd
from unittest.mock import Mock, patch
from app.data_formatting import format_as_is_data, format_to_be_data

@pytest.fixture
def mock_diarization_pipeline():
    pipeline = Mock()
    pipeline.return_value.itertracks.return_value = [
        (Mock(start=0, end=1), None, "speaker1"),
        (Mock(start=1, end=2), None, "speaker2")
    ]
    return pipeline

@pytest.fixture
def mock_openai_client():
    client = Mock()
    client.audio.transcriptions.create.return_value = Mock(text="Test transcription")
    return client

def test_format_to_be_data():
    as_is_data = pd.DataFrame({
        'timestamp': ['2023-01-01 00:00:00', '2023-01-01 00:00:01'],
        'speaker': ['speaker1', 'speaker2'],
        'asis_stt_fragment': ['Hello', 'World']
    })

    result = format_to_be_data(as_is_data)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert list(result.columns) == ['contract_id', 'call_id', 'start_time', 'end_time', 'aggregated_stt']
    assert result['aggregated_stt'].iloc[0] == 'Hello | World'
    assert result['start_time'].iloc[0] == '2023-01-01 00:00:00'
    assert result['end_time'].iloc[0] == '2023-01-01 00:00:01'