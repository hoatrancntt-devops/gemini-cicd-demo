pipeline {
    agent any
    environment {
        HARBOR_URL = 'harbor.devopsviet.io.vn'
        PROJECT_NAME = 'gemini-project'
        APP_NAME = 'my-gemini-app'
        IMAGE_TAG = "v1.${BUILD_NUMBER}"
        HARBOR_CRED = 'harbor-creds'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build & Push Docker Image') {
            steps {
                script {
                    docker.withRegistry("https://${HARBOR_URL}", "${HARBOR_CRED}") {
                        def appImage = docker.build("${HARBOR_URL}/${PROJECT_NAME}/${APP_NAME}:${IMAGE_TAG}")
                        appImage.push()
                        appImage.push("latest")
                    }
                }
            }
        }
        stage('Package & Push Helm Chart') {
            steps {
                script {
                    dir('charts/my-gemini-app') {
                        withCredentials([usernamePassword(credentialsId: "${HARBOR_CRED}", usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                            sh "helm registry login ${HARBOR_URL} --username $USER --password $PASS --insecure"
                        }
                        sh "helm package . --version 1.0.${BUILD_NUMBER} --app-version ${IMAGE_TAG}"
                        sh "helm push ${APP_NAME}-1.0.${BUILD_NUMBER}.tgz oci://${HARBOR_URL}/${PROJECT_NAME}"
                    }
                }
            }
        }
    }
}
