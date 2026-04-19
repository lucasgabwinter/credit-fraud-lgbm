import json
from src.lambda_handler import lambda_handler
from unittest.mock import Mock, patch

event = {
    "Records": [
        {
            "body": json.dumps({
                "transaction_id": "tx_001",
                "features": {
                    "V1": -1.271244,
                    "V2": 2.462675,
                    "V3": -2.851395,
                    "V4": 2.324480,
                    "V5": -1.372245,
                    "V6": -0.948196,
                    "V7": -3.065234,
                    "V8": 1.166927,
                    "V9": -2.268771,
                    "V10": -4.881143,
                    "V11": 2.255147,
                    "V12": -4.686387,
                    "V13": 0.652375,
                    "V14": -6.174288,
                    "V15": 0.594380,
                    "V16": -4.849692,
                    "V17": -6.536521,
                    "V18": -3.119094,
                    "V19": 1.715494,
                    "V20": 0.560478,
                    "V21": 0.652941,
                    "V22": 0.081931,
                    "V23": -0.221348,
                    "V24": -0.523582,
                    "V25": 0.224228,
                    "V26": 0.756335,
                    "V27": 0.632800,
                    "V28": 0.250187,
                    "Amount": 0.01
                }
            })
        }
    ]
}
with patch("src.lambda_handler.get_table") as mock_get_table:
    mock_table = Mock()
    mock_get_table.return_value = mock_table

    result = lambda_handler(event, None)
    print(result)
    json.dumps(result)
