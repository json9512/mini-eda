# mini-eda

- [localstack](https://localstack.cloud/)이라는 간단한 툴을 사용해서 producer-channel-consumer를 구현함
- producer: node koa server로 sns에 publish 할 수 있도록 구현
- channel: 현재 우리가 사용하고 있는 SNS - SQS 구조를 가지고 있음
- consumer: js로 작성된 lambda 워커 (commonjs 형식)

## 주 목적

- 현재 우리 인프라와 유사하게 구성한 상태에서 `메세지의 형태`를 어떻게 실험해보면 좋을지 테스트하기 위함
- ex) SNS, SQS의 메세지 크기 제한 설정된 상태에서 어떤 값들을 포함해야하는지
- ex) SNS, SQS에서 어떤 속성들을 사용하면 되는지. 예를 들면 Message Attribute
- ex) SQS에서 메세지 꺼내는 순서 테스트 등

## 유의사항

- AWS 서비스를 표방하고는 있지만 100% 동일한 구현은 아니라서 outdated 되어있는 것들이 종종 있음
- 몇몇개의 서비스는 유료 플랜으로 결제해야함
- **참고 목적으로만 사용할 예정**

<br />

# 실행 방법

- root directory (이 readme가 있는 위치)에서 `docker-compose up` 실행
  - docker-compose가 없다면 다운받으면 됨: https://docs.docker.com/compose/install/linux/
  - 아마 docker desktop이 설치되어있다면 같이 설치되었을 가능성있음
- 처음 설치하는데 오래 걸림
- 이상한 로그가 터미널에 촤라라라라락 올라와야함. prefix: `localstack_main` 또는 `mini-eda`가 붙어있을거임
- 일단 정상적으로 로그들이 올라오면 ctrl+c를 하고 `docker-compose down`을 실행
  - 에러 로그 비스무리한게 보이면 [@junghyun](junghyun@publy.co) 호출
  - EntryPoint 뭐시기 관련 에러는 무시해도 좋음
- 다시 `docker-compose up`을 실행 (깔끔하게 셋업이 가끔 안되는 경우가 있어서...)
- 정상적으로 처리되면 `app.localstack.cloud` 접속
- github 아이디로 연결
- 우측 상단 알림벨 옆에 서버를 `ap-southeast-2`로 변경
- resources에서 SQS, SNS, Lambda에 별표 표시
- Dashboard로 돌아가면 별표 표시한것들이 보임
- 자유롭게 둘러보면됩니다. 이미 생성된 SNS, SQS, Lambda가 보여야함

## 기억할 것

- `docker-compose up`: 프로젝트 실행
  - ctrl+c 하면 실행 종료. 실행 종료하면 항상 `docker-compose down`을 같이 해주셔야함
- 만약 코드 수정 사항이 생기면 docker desktop에서 해당 image와 container를 삭제해주고 `docker-compose up` 해주시면 깔끔하게 변경사항 반영됨
  - 주로 `localstack/localstack` 이미지는 건드릴 필요는 없고 `public.ecr.aws/lambda/nodejs:18` (람다) 이미지와 `mini-eda`를 삭제해줘야함
- ~~hot reload 같은 엘레강트한 기능따위 없으니 `docker-compose up/down` 과 친해져야함~~
  - 하다보니 ~~빡쳐서~~ 너무 접근성이 안좋아서 hot reload 구현함
  - 다만, producer만 가능하고 (코드 수정하면 바로 반영됨)
  - consumer의 경우는 zip 해서 올리는 형태기 때문에 `docker-compose up/down` 해주셔야함
  - SNS, SQS 설정을 바꾸는거라면 (ex. setup.py 쪽 스크립트) 이것도 `docker-compose up/down` 해주셔야함
- `volume/logs/localstack_infra.err`를 참고하면 로그가 다 기록되고 있음

# 간단 설명

- `docker-compose.yml`이 전체 인프라 설정을 해줌. 여기서 `setup` 폴더에 있는 `Dockerfile` 호출
- `setup/Dockerfile`을 따라서 python 가상 환경을 만들고 `setup.py` 호출
- `setup.py`에서 `awscli`를 통해 AWS 인프라를 로컬하게 만들고 있음
  - (Dockerfile에서 걍 RUN 하면 되는거 아닌가 싶나요? 왜 이렇게 했는지 묻지마요 ㅎ ~~하다보니 이렇게 됐어요~~)
- 인프라가 정상적으로 올라가면:
  - localstack에서 정의한 SNS, SQS, Lambda를 사용함
  - producer는 localstack/SNS로 토픽을 publish 할 수 있음 (구현 예정)
  - localstack/SNS는 해당 사항을 localstack/SQS로 전파
  - localstack/SQS는 메세지가 들어오면 연결된 Lambda를 실행 (lambda 도커 이미지가 없다면 cold start임)

# 간단한 테스트

- app.localstack.cloud에서 SQS로 이동
- SEND MESSAGE 클릭
- Queue Url에 정의된 SQS가 떠야함. 아무거나 하나 클릭
- Message Body 아무거나 입력 후 SEND 클릭
- 터미널 로그에서 해당 메세지 로그가 떠야함
  - consumer 코드를 보면 해당 event를 `console.log` 하도록 해놨음


---

### 프로젝트 셋업 테스트 Log

- 03.07: window + macos에서 정상적으로 동작하는 것 확인
- 03.12: producer 기본 설정 끝남. SNS 기능만 추가하면 됨
