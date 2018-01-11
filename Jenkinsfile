/** Desired capabilities */
def capabilities = [
  browserName: 'Firefox',
  version: '57.0',
  platform: 'Windows 10'
]

pipeline {
  agent {label 'mesos-testing'}
  libraries {
    lib('fxtest@1.9')
  }
  options {
    ansiColor('xterm')
    timestamps()
    timeout(time: 1, unit: 'HOURS')
  }
  environment {
    VARIABLES = credentials('MOZILLIANS_VARIABLES')
    PYTEST_ADDOPTS =
      "--tb=short " +
      "--color=yes " +
      "--driver=SauceLabs " +
      "--variables=capabilities.json " +
      "--variables=${VARIABLES}"
    SAUCELABS = credentials('SAUCELABS')
  }
  stages {
    stage('Lint') {
      steps {
        sh "tox -e flake8"
      }
    }
    stage('Test') {
      steps {
        writeCapabilities(capabilities, 'capabilities.json')
        sh "tox -e py27"
      }
      post {
        always {
          archiveArtifacts 'results/*'
          junit 'results/*.xml'
          publishHTML(target: [
            allowMissing: false,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: 'results',
            reportFiles: "py27.html",
            reportName: 'HTML Report'])
        }
      }
    }
  }
}
