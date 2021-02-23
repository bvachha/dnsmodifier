import React from "react";

class AddZoneForm extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      name:null,
      rname:null,
      nameserver:null
    }
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  } 

  handleChange(event){
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
        nameserver: this.state.nameserver
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
        <input class="form-control"
                type="text"
                name="name"
                placeholder="example.com.(Enter a canonical name)"
                 value={this.state.name}/>
        <br/>
        <label class="form-label">NameServers</label>
        <input class="form-control" type="text" name="nameserver" placeholder='nameserver1.example.com (Enter the primary name server)'
        value={this.state.nameservers}/>
        <br/>
        <label class="form-label">Admin Email</label>
        <input class="form-control" type="text" name="rname" placeholder="hostadmin@example.com" value={this.state.rname}/>
        <br/>
        <input type="submit" value="Add Zone" />
        <button class="btn btn-primary" onClick={this.props.backButton}>Go back</button>
      </form>
    </div>
    );
    }
}

export default AddZoneForm;