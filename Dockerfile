FROM public.ecr.aws/lambda/python:3.14

RUN dnf install -y libgomp && dnf clean all

COPY requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

COPY src ${LAMBDA_TASK_ROOT}/src
COPY artifacts ${LAMBDA_TASK_ROOT}/artifacts

CMD ["src.lambda_handler.lambda_handler"]
