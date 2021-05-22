#!/usr/bin/env python3

import yaml
from jinja2 import Template
from datetime import datetime
from kubernetes import client, config

def main():
    kaniko("sidecar", "latest", "git://github.com/kbase/init-sidecar.git")

def kaniko(image, tag, repo):
    # Set image name, and consistent timestamp
    build_image_name = image
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')

    # Set variables to be set in the template
    data = {
        "image_name": build_image_name + "-" + timestamp,
        "image_tag": tag,
        "repo_name": repo,
    }
    # Render YAML from Jinja template
    with open('kaniko-template.j2') as file_:
        j2_template = Template(file_.read())
    build_yaml = j2_template.render(data)
    # Begin K8s deploymnent
    config.load_kube_config()
    dep = yaml.safe_load(build_yaml)
    k8s_apps_v1 = client.CoreV1Api()
    resp = k8s_apps_v1.create_namespaced_pod(
        body=dep, namespace="next")
    print("Deployment created. status='%s'" % resp.metadata.name)

if __name__ == '__main__':
    main()
