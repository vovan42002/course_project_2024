pipeline {
    environment {
        DOCKER_CREDS = credentials('docker-registry-rw')
        DOCKER_REGISTRY_HOST = 'docker.io'
        DOCKER_CONFIG = "${WORKSPACE}/.docker"
        DOCKER_IMAGE_NAME = 'docker.io/vovan4/course-project-2024/backend'
    }
    options {
        buildDiscarder(logRotator(daysToKeepStr:'14'))
    }
    stages {
        stage('Prepare environment for build') {
            steps {
                script {
                    switch (GIT_BRANCH) {
                        case 'master':
                            dockerTag = 'latest'
                            break
                        default:
                            dockerTag = 'feature'
                            helmTag = ''
                            break
                    }
                }
            }
        }

        stage('Build Docker image') {
            steps {
                sh label: "Build ${APP_NAME} image", script:
                    """
                    docker build -f api_gw/Dockerfile api_gw \
                      --label GIT_REVISION=\$(git rev-parse HEAD 2>/dev/null) \
                      --label GIT_COMMIT_DATE='\$(git show -s --format=%ci HEAD 2>/dev/null)' \
                      -t ${DOCKER_IMAGE_NAME}:${dockerTag}
                    """
            }
        }

        stage('Publish Docker image') {
            when {
                anyOf { branch 'master'; buildingTag() }
            }
            steps {
                sh label: 'Docker login', script: "docker login --username ${DOCKER_CREDS_USER} --password ${DOCKER_CREDS_PASSWORD} ${DOCKER_REGISTRY_HOST}"
                sh label: "Publish ${APP_NAME} image", script:
                """
                docker push ${DOCKER_IMAGE_NAME}:${dockerTag}
                docker rmi ${DOCKER_IMAGE_NAME}:${dockerTag} || true
                """
            }
            post {
                always {
                    sh "docker logout ${DOCKER_REGISTRY_HOST}"
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
        failure {
            emailext attachLog: true, body: "${currentBuild.currentResult}: Job ${env.JOB_NAME} build ${env.BUILD_NUMBER}",
            subject: "Jenkins Build ${currentBuild.currentResult}: Job ${env.JOB_NAME}",
            recipientProviders: [[$class: 'DevelopersRecipientProvider']]
        }
    }
}
