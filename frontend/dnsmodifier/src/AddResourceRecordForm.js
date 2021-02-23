import React from "react";

class AddResourceRecordForm extends React.Component{
    constructor(props){
      super(props);
      this.state = {
        domain_id: this.props.zoneId,
        name: null,
        type: null,
        content:null,
        ttl:3600,
        priority:10
      }
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleChange(event){
      let name = event.target.name;
      this.setState({
        [name]: event.target.value
      });
    }
  
    handleSubmit(event){
      event.preventDefault();
      fetch("http://127.0.0.1:5000/api/zone-records/",{
        method: "POST",
        body: JSON.stringify({
          zone_id:parseInt(this.state.domain_id),
          name:this.state.name,
          type: this.state.type,
          content:this.state.content,
          ttl: parseInt(this.state.ttl),
          priority:parseInt(this.state.priority)
        }),
        headers:{"api-key":process.env.REACT_APP_API_KEY}
      })
      .then(response =>response.json())
      .then(json=>{
        if (json["error"]){
          alert("ERROR: "+ json["error"]);
        }
        else{
          alert("Record created Successfully");
          this.props.backFunc()
        }
      })
    }
  
  
    render(){
      return(
        <div>
        <h2> Add new resource record </h2>
        <form  onSubmit={this.handleSubmit} onChange={this.handleChange}>
          <label class="form-label">Name</label>
          <input class="form-control"
          type="text" name="name"
          value={this.state.name}
          placeholder="For sub.example.com in example.com zone, type sub. Leave Blank for zone level records" />
          <br/>
          <label class="form-label">Type</label>
          <input class="form-control" type="text" name="type" value={this.state.type}
          placeholder="Accepted types: NS,MX,A,TXT,CNAME"/>
          <br/>
          <label class="form-label">Content</label>
          <input class="form-control" type="text" name="content" value={this.state.content}
          placeholder="Content of the record"/>
          <br/>
          <label class="form-label">TTL</label>
          <input class="form-control" type="text" name="ttl" value={this.state.ttl} />
          <br/>
          <label class="form-label">Priority</label>
          <input class="form-control" type="text" name="priority" value={this.state.priority} />
          <input type="submit" class="btn btn-success" value="Add Record" />
          <button class="btn btn-success" onClick={this.props.backFunc}>Go back</button>
        </form>
      </div>
      )
    }
  }

  export default AddResourceRecordForm;