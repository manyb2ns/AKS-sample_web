pipeline {
    agent any

    environment {
        ACR_LOGINSERVER = "jdbacr.azurecr.io"
        ACR_ID = "jdbacr"
        ACR_PASSWORD = credentials('ACR_PASSWORD')
        GITHUB_CREDENTIALS = credentials('GITHUB_TOKEN')
        commitHash = ""
        IMAGE_NAME = "jenkins-ci-test"
        CONTAINER_NAME = "jenkins-ci-test-container"
        REPO_URL = "https://github.com/manyb2ns/AKS-sample_web.git"
        BRANCH_NAME = "dev-jdb"
        APP_PORT = "5000"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning repository..."

                // 현재 커밋 해시 가져오기
                def commitHash = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                echo "Current Commit Hash: ${commitHash}"

                // 디렉토리 초기화 및 clone
                sh """
                pwd && ls -al
                rm -rf ./* ./.git || true
                git clone --branch ${BRANCH_NAME} ${REPO_URL} .
                mkdir -p ./static
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }
        stage('Run Docker Container') {
            steps {
                echo "Starting Docker container..."
                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:${APP_PORT} ${IMAGE_NAME}
                """
            }
        }

        stage('Web Page Request') {
            steps {
                echo "Sending request to Flask application..."
                script {
                    def response = sh(
                        script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:${APP_PORT}",
                        returnStdout: true
                    ).trim()
                    echo "Response code: ${response}"
                    if (response != "200") {
                        error "Application did not respond with HTTP 200. Check your application logs."
                    }
                }
            }
        }

        stage('Upload Image to ACR') {
          steps{
            echo "Uploading Image to ACR..."
            sh """
              docker login ${ACR_LOGINSERVER} -u ${ACR_ID} -p ${ACR_PASSWORD}
              docker tag ${IMAGE_NAME} ${ACR_LOGINSERVER}/${IMAGE_NAME}:latest
              docker push ${ACR_LOGINSERVER}/${IMAGE_NAME}:latest
            """
          }
        }
  }

    post {
        success {
            script {
                updateGitHubStatus(commitHash, 'SUCCESS', 'Pipeline succeeded.')
            }
        }
        failure {
            script {
                updateGitHubStatus(commitHash, 'FAILURE', 'Pipeline failed.')
            }
        }
    }
}

// GitHub 상태 업데이트 함수
def updateGitHubStatus(commitHash, status, description) {
    echo "Updating GitHub Status:"
    echo "Commit: ${commitHash}"
    echo "State: ${status}"
    echo "Description: ${description}"

    sh """
    curl -X POST -u ${GITHUB_CREDENTIALS} \
        -H "Accept: application/vnd.github.v3+json" \
        https://api.github.com/repos/manyb2ns/AKS-sample_web/statuses/${commitHash} \
        -d '{
            "state": "${status.toLowerCase()}",
            "description": "${description}",
            "context": "Jenkins CI"
        }'
    """

}