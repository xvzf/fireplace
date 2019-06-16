# Fireplace Server & Client deployment /Testing/Development)
> This setup is intendet to run on Kubernetes; tested on [k3s](https://k3s.io/).
> **WARNING** Not for production use
> **ATTENTION** Everything is kept inside the `fireplace` namespace

You can deploy everything to a running cluster using `make all`.
Keep in mind you have to initialize the database (e.g.):
```
$ cd $REPO_ROOT/assets
$ kubectl -n fireplace port-forward svc/timescaledb 5432:5432 &
$ make
$ fg
$ ctrg+c
```

## Components
- Timescaledb Database with persistent storage (Statefulset)
- Fireplace Server Deployment (accessable via service `fireplace-server`)
- Fireplace random data Client Deployment (accessable via service `fireplace-client`)

## Making the test-setup accessable
> Note: Our test-system is reachable [here](http://server.fireplace.spankmewithcat6.de/swagger/) (e.g. openapi endpoint)

You have to adapt the host names defined in `ingress.yaml`! If you do not have a public DNS, you can use a service like [xip.io](https://xip.io/)