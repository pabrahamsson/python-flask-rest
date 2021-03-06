#!/usr/bin/groovy

////
// This pipeline requires the following plugins:
// Kubernetes Plugin 0.10
////

String ocpApiServer = env.OCP_API_SERVER ? "${env.OCP_API_SERVER}" : "https://openshift.default.svc.cluster.local"

node('master') {

  env.NAMESPACE = readFile('/var/run/secrets/kubernetes.io/serviceaccount/namespace').trim()
  env.TOKEN = readFile('/var/run/secrets/kubernetes.io/serviceaccount/token').trim()
  env.OC_CMD = "oc --token=${env.TOKEN} --server=${ocpApiServer} --certificate-authority=/run/secrets/kubernetes.io/serviceaccount/ca.crt --namespace=${env.NAMESPACE}"

  env.APP_NAME = env.JOB_NAME.replaceAll(/-?pipeline-?/, '').replaceAll(/-?${env.NAMESPACE}-?/, '').replaceAll(/\//, '')
  def projectBase = env.NAMESPACE.replace(/-build/, '')
  env.STAGE1 = "${projectBase}-dev"
  env.STAGE2 = "${projectBase}-stage"
  env.STAGE3 = "${projectBase}-prod"

}

node('python') {
  stage('SCM Checkout') {
    checkout scm
  }

  stage('Unit Test') {
    sh "pip install --user -r requirements.txt"
    sh "nosetests --with-xunit --with-coverage --cover-test --cover-package=wsgi --cover-erase -v"
  }

  stage('Generate coverage report') {
    sh "python -m coverage xml"
    cobertura autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: 'coverage.xml', conditionalCoverageTargets: '70, 0, 0', failUnhealthy: false, failUnstable: false, lineCoverageTargets: '80, 0, 0', maxNumberOfBuilds: 0, methodCoverageTargets: '80, 0, 0', onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false
  }

  stage('SonarQube Analysis') {
    sh "unset JAVA_TOOL_OPTIONS && sonar-scanner -Dsonar.host.url=http://${SONARQUBE_SERVICE_HOST}:${SONARQUBE_SERVICE_PORT}"
  }

  stage('Build Image') {

    sh """
      ${env.OC_CMD} start-build ${env.APP_NAME} --from-dir=. --wait=true --follow=true || exit 1
    """
  }

  stage("Promote to ${env.STAGE1}") {
    sh """
    ${env.OC_CMD} tag ${env.NAMESPACE}/${env.APP_NAME}:latest ${env.STAGE1}/${env.APP_NAME}:latest
    """
  }

  stage("Verify Deployment to ${env.STAGE1}") {

    openshiftVerifyDeployment(deploymentConfig: "${env.APP_NAME}", namespace: "${STAGE1}", verifyReplicaCount: true)

    input "Promote Application to Stage?"
  }

  stage("Promote To ${env.STAGE2}") {
    sh """
    ${env.OC_CMD} tag ${env.STAGE1}/${env.APP_NAME}:latest ${env.STAGE2}/${env.APP_NAME}:latest
    """
  }

  stage("Verify Deployment to ${env.STAGE2}") {

    openshiftVerifyDeployment(deploymentConfig: "${env.APP_NAME}", namespace: "${STAGE2}", verifyReplicaCount: true)

    input "Promote Application to Prod?"
  }

  stage("Promote To ${env.STAGE3}") {
    sh """
    ${env.OC_CMD} tag ${env.STAGE2}/${env.APP_NAME}:latest ${env.STAGE3}/${env.APP_NAME}:latest
    """
  }

  stage("Verify Deployment to ${env.STAGE3}") {

    openshiftVerifyDeployment(deploymentConfig: "${env.APP_NAME}", namespace: "${STAGE3}", verifyReplicaCount: true)

  }
}

println "Application ${env.APP_NAME} is now in Production!"
