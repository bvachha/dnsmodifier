<h1>DNS Record modification project</h1>

This project is a playground environment to learn DNS and building a functional frontend to manipulate the records
stored within.

The application is a frontend app written in ReactJS that communicates with a REST API backend to retrieve and send
data to the underlying DNS server.

<h2>Environment Variables</h2>
The following environment variables are needed by the API server to function
APP_SECRET_KEY='APP secret value'
API_KEY='API key value for accepting incoming connections'
REACT_APP_API_KEY="Api key that REACT frontend uses to authenticate with API server"

<h2>API Endpoints</h2>

<h3>/api/zones</h3>

Allowed methods: GET, POST, DELETE

**GET /api/zones/**

Retrieves the list of zones on the dns server for which the DNS is Authoritative with their ids.

**POST /api/zones/**

Post method on this endpoint will create a zone on the server and set up an SOA record and at least one nameserver record

To create a new zone, the http request must have a json body with the following parameters in the body of the request

```
{
    "name": "canonical name for the zone",
    "rname": email address of the responsible party for the zone,
    "nameserver": "Hostname of primary name server"
}
```

**DELETE /api/zones/?id=< zone id >**

This endpoint allows the deletion of the zone specified by the zone id. It will also remove all the resource records associated with the zone from the rrset tables.


<h3>/api/zone-records</h3>

Allowed methods: GET, POST, DELETE

***GET /api/zone-records/?id=<zone_id>***

This endpoint retrieves all the records available with the server for a given zone id.

***DELETE /api/zone-records/?id=<record_id>***

Using the delete method on this endpoint with a valid record_id will instruct the server to delete the specified resource record from its database

***POST /api/zone-records/?id=<zone_id>*** 

Handles the creation of a new resource record with the parameters specified in the body of the request

The parameters that are used by the endpoint are 

```
{
    "name": "name for the subdomain for which the content is specified, the zone name is always appended to the value here",
    "type": "Type of record being added to the database. Only supports specific types",
    "content": "the content of the resource record"
    "ttl": "optional ttl value to specify"
    "priority": "optional priority value, discarded if the record type does not support it" 
}
```

<h2>DEPLOYMENT WITH DOCKER</h2>
1. Create the environment file using the sample template .env.sample
1. The API key values must be the same for API_KEY and REACT_APP_API_KEY
1. Switch to the root of the project directory and run 
   ```
   sudo docker build -t dnsmod . 
   ```
1. Wait for the image to be built
1. deploy the application using the following command
```
docker run -it --env-file <name of env file> -p 5300:53/udp -p 3000:3000/tcp -p 5000:5000/tcp dnsmod:latest
```
1. You can now view the admin console on ```http://localhost:3000/```
1. On making changes, you can verify that the changes are being served by pointing dig or any other dns tool to port 5300 on localhost and querying the DNS server there.


