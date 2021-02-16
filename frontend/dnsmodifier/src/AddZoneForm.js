import React from "react";

class AddZoneForm extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      name:null,
      rname:null,
      nameservers:null
    }
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  } 

  handleChange(event){
    event.preventDefault();
    const name = event.target.name;
    this.setState({
      [name]:event.target.value
    });
  }



  handleSubmit(event){
    event.preventDefault();
    fetch("http://127.0.0.1:5000/api/zones/",{
      method: "POST",
      body: JSON.stringify({
        name: this.state.name,
        rname: this.state.rname,
        nameservers: JSON.parse(this.state.nameservers)
      }),
      headers:{"api-key":process.env.REACT_APP_API_KEY}
    })
    .then(response=>response.json())
    .then(json=>{
      if (json["error"]){
        alert(json["error"]);
        
      }
      else{
        alert("Zone record created successfully");
        this.props.backButton();
      }
    })
  }

  render(){
    return(
    <div>
      <h2> Add new zone record </h2>
      <form  onSubmit={this.handleSubmit} onChange={this.handleChange}>
        <label class="form-label">ZoneName</label>
        <input class="form-control" type="text" name="name" value={this.state.name} />
        <br/>
        <label class="form-label">NameServers</label>
        <input class="form-control" type="text" name="nameservers" value={this.state.nameservers} />
        <br/>
        <label class="form-label">Admin Email</label>
        <input class="form-control" type="text" name="rname" value={this.state.rname} />
        <br/>
        <input type="submit" value="Add Zone" />
        <button class="btn btn-primary" onClick={this.props.backButton}>Go back</button>
      </form>
    </div>
    );
    }
}

export default AddZoneForm;