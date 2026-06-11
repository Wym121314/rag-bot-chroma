"""
Shared test fixtures for RAG PDFBot tests.
"""

import pytest


@pytest.fixture
def sample_chinese_text():
    """Sample Chinese car manual text for testing."""
    return """
[文档: test_manual.pdf | 第1页]
续航里程：606公里（CLTC工况）
电池容量：75.0 kWh
快充时间：30分钟可达80%

[文档: test_manual.pdf | 第2页]
车身尺寸：长4694mm × 宽1850mm × 高1443mm
轴距：2875mm
整备质量：1836kg
百公里加速：5.6秒
"""


@pytest.fixture
def sample_chunks():
    """Sample text chunks for testing."""
    return [
        "续航里程：606公里（CLTC工况）",
        "电池容量：75.0 kWh",
        "快充时间：30分钟可达80%",
        "车身尺寸：长4694mm × 宽1850mm × 高1443mm",
    ]
