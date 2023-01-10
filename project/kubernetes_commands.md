# Kubernetes Commands

## Deploy a Kubernetes cluster

1. Create a vagrant box and ssh into it

    ```bash
    vagrant up

    vagrant ssh
    ```

    ![Vagrant up](/images/08-vagrant-up.jpg)
    ![Vagrant ssh](/images/09-vagrant-ssh.jpg)

2. Install the Lightweight Kubernetes in the Vagrant VM

    ```bash
    curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644
    sudo su
    k3s kubectl get node
    ```

    ![Install k3s](/images/10-k3s-install.jpg)

    ```bash
    kubectl cluster
    kubectl get nodes
    kubectl get nodes -o wide
    ```

    ![Kubectl get nodes](/images/11-k3s-nodes.jpg)

3. Deploy TechTrends with Kubernetes manifests

    ```bash
    # copy the manifests to the vagrant box
    vagrant upload kubernetes /home/vagrant/kubernetes

    # deploy the manifests
    kubectl apply -f /home/vagrant/kubernetes/

    kubectl get all -n sandbox
    ```

    ![Kubectl get all](/images/12-k3s-get-all.jpg)

4. Installing Helm

    ```bash
    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
    chmod 700 get_helm.sh
    ./get_helm.sh
    ```

5. Installing ArgoCD

    ```bash
    kubectl create namespace argocd
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

    kubectl get pods -n argocd

    kubectl get svc -n argocd
    ```

    ```bash
    cat << EOF > argocd-server-nodeport.yaml
    apiVersion: v1
    kind: Service
    metadata:
      annotations:
      labels:
        app.kubernetes.io/component: server
        app.kubernetes.io/name: argocd-server
        app.kubernetes.io/part-of: argocd
      name: argocd-server-nodeport
      namespace: argocd
    spec:
      ports:
      - name: http
        port: 80
        protocol: TCP
        targetPort: 8080
        nodePort: 30077
      - name: https
        port: 443
        protocol: TCP
        targetPort: 8080
        nodePort: 30088
      selector:
        app.kubernetes.io/name: argocd-server
      sessionAffinity: None
      type: NodePort
    EOF
    ```

    ```bash
    kubectl apply -f argocd-server-nodeport.yaml

    kubectl get svc -n argocd
    ```

    ![ArgoCD get svc](/images/13-argocd-get-svc.jpg)
  
    ```bash
    # get the password
    kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

    # login to the UI
    http://localhost:8080
    ```
  
    ![ArgoCD login](/images/14-argocd-login.jpg)
    ![ArgoCD UI](/images/15-argocd-ui.jpg)

## Deploy TechTrends with ArgoCD

1. Upload Manifests to the Vagrant VM

  ```bash
  vagrant upload argocd/
  ```

2. Deploy the Application in ArgoCD

  ```bash
  kubectl apply -f argocd/helm-techtrends-prod.yaml
  kubectl apply -f argocd/helm-techtrends-staging.yaml

  kubectl get application -n argocd
  ```

  ![ArgoCD get application](/images/16-argocd-get-application.jpg)

3. Access the ArgoCD UI

  ![ArgoCD UI](/images/17-argocd-techtrends.jpg)

4. Sync Applications

  ![ArgoCD Sync Staging](/images/18-argocd-techtrends-staging.jpg)
  ![ArgoCD Sync Staging](/images/18-argocd-techtrends-staging-2.jpg)
  ![ArgoCD Sync Staging](/images/18-argocd-techtrends-staging-3.jpg)
