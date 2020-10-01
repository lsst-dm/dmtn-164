from diagrams import Diagram
from diagrams.k8s.compute import DaemonSet, Deployment, Pod, ReplicaSet
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.podconfig import ConfigMap
from diagrams.k8s.group import Namespace

with Diagram("JupyterHub Kubernetes Architecture", show=False):
    nublado_ns = Namespace("nublado")
    pp_net = Ingress("/pp")
    nb_net = Ingress("/nb")

    pp_svc = Service("Prepuller")
    pp_deploy = Deployment("Prepuller")
    pp_pod = Pod("Prepuller")
    pp_ds = DaemonSet("Single image puller")

    hub_config = ConfigMap("Hub Config YAML")

    hub_svc = Service("JupyterHub")
    hub_deploy = Deployment("JupyterHub")
    hub_pod = Pod("JupyterHub")

    proxy_svc = Service("JupyterHubProxy")
    proxy_deploy = Deployment("JupyterHubProxy")
    proxy_pod = Pod("JupyterHubProxy")

    user_ns = Namespace("nublado-lsptestuser01")
    user_lab_pod = Pod("JupyterLab pod")
    user_config = ConfigMap("Lab Config YAML + Token")

    nublado_ns >> nb_net >> proxy_svc >> proxy_deploy >> proxy_pod >> hub_svc
    nublado_ns >> pp_net >> pp_svc >> pp_deploy >> pp_pod >> hub_config >> pp_pod >> pp_ds

    hub_config >> hub_pod >> hub_config
    hub_svc >> hub_deploy >> hub_pod
    user_ns >> user_lab_pod >> user_config
    proxy_pod >> user_lab_pod
