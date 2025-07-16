pipeline {
  agent any

  environment {
    DOCKER_REGISTRY = "docker.io"
    FRONTEND_IMAGE = "fierdakcap/weather-frontend"
    BACKEND_IMAGE = "fierdakcap/weather-backend"
    DOCKERHUB_CREDENTIALS_ID = 'dockerhub-credentials'  // Jenkins credentials ID
  }

  options {
    skipDefaultCheckout(true)
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Test Backend') {
      agent { label 'python' }
      environment {
        OPENWEATHER_API_KEY = credentials('openweather-api-key')
        WEATHER_API_BASE_URL = credentials('weather-api-base-url')
      }
      steps {
        dir('backend') {
          sh '''
            python3 -m venv venv
            . venv/bin/activate
            pip install -r requirements.txt
            PYTHONPATH=. pytest tests/ -v --cov=app --cov-report=xml
            flake8 app/ --max-line-length=88 || echo "Linting issues found but not blocking"
          '''
          junit 'tests/**/*.xml'
          publishCoverage adapters: [coberturaAdapter('coverage.xml')]
        }
      }
    }

    stage('Test Frontend') {
      agent { label 'nodejs' }
      steps {
        dir('frontend') {
          sh '''
            rm -rf node_modules package-lock.json
            npm ci
            npx eslint . --report-unused-disable-directives --max-warnings 0
            npm test
          '''
          // Optional: If using Jenkins plugins for frontend coverage
          // publishHTML(target: [allowMissing: false, alwaysLinkToLastBuild: true, keepAll: true, reportDir: 'coverage', reportFiles: 'lcov-report/index.html', reportName: 'Frontend Coverage'])
        }
      }
    }

    stage('Build & Push Backend Image') {
      when {
        branch 'main'
      }
      steps {
        dir('backend') {
          script {
            docker.withRegistry("https://${env.DOCKER_REGISTRY}", "${env.DOCKERHUB_CREDENTIALS_ID}") {
              def image = docker.build("${BACKEND_IMAGE}:${env.BUILD_NUMBER}")
              image.push()
              image.push('latest')
            }
          }
        }
      }
    }

    stage('Build & Push Frontend Image') {
      when {
        branch 'main'
      }
      steps {
        dir('frontend') {
          script {
            docker.withRegistry("https://${env.DOCKER_REGISTRY}", "${env.DOCKERHUB_CREDENTIALS_ID}") {
              def image = docker.build("${FRONTEND_IMAGE}:${env.BUILD_NUMBER}")
              image.push()
              image.push('latest')
            }
          }
        }
      }
    }
  }

  post {
    failure {
      mail to: 'yourteam@example.com',
           subject: "CI/CD Failed: ${env.JOB_NAME} [#${env.BUILD_NUMBER}]",
           body: "See details: ${env.BUILD_URL}"
    }
  }
}
