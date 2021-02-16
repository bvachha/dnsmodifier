import React from "react";

class EditResourceRecordForm extends React.Component{
    constructor(props){
      super(props);
      this.state = {
        id: this.props.recordData.id,
        domain_id: this.props.recordData.zoneId,
        name: this.props.recordData.name,
        type: this.props.recordData.type,
        content:this.props.recordData.content,
        ttl:this.props.recordData.ttl,
        priority: this.props.recordData.priority ? this.props.recordData.priority : 0
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
            method:"POST",
            body:JSON.stringify({
               id:this.state.id,
               zone_id:this.state.domain_id,
               name:this.state.name,
               type:this.state.type,
               content:this.state.content,
               ttl:parseInt(this.state.ttl),
               priority: parseInt(this.state.priority), 
            }),
            headers:{"api-key":process.env.REACT_APP_API_KEY}
        })
        .then(response => response.json())
        .then(json => {
            if (json["error"]){
                alert("ERROR: " + json["error"]);
            }
            else{
                alert("Record updated successfully");
                this.props.backFunc();
            }
        })
    }
  
  
    render(){
      return(
        <div>
        <h2> Edit resource record </h2>
        <form  onSubmit={this.handleSubmit} onChange={this.handleChange}>
          <label class="form-label">Name</label>
          <input class="form-control" type="text" name="name" value={this.state.name} readOnly/>
          <br/>
          <label class="form-label">Type</label>
          <input class="form-control" type="text" name="type" value={this.state.type} readOnly/>
          <br/>
          <label class="form-label">Content</label>
          <input class="form-control" type="text" name="content" value={this.state.content} />
          <br/>
          <label class="form-label">TTL</label>
          <input class="form-control" type="text" name="ttl" value={this.state.ttl} />
          <br/>
          <label class="form-label">Priority</label>
          <input class="form-control" type="text" name="priority" value={this.state.priority} />
          <input type="submit" class="btn btn-success" value="Update Record" />
          <button class="btn btn-success" onClick={this.props.backFunc}>Go back</button>
        </form>
      </div>
      )
    }
  }
  
export default EditResourceRecordForm