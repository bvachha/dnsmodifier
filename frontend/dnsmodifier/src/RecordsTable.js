import React from "react"
import { confirmAlert } from "react-confirm-alert"
import 'react-confirm-alert/src/react-confirm-alert.css'
import AddResourceRecordForm from "./AddResourceRecordForm"
import EditResourceRecordForm from "./EditResourceRecordForm"

class ZoneRecordsTable extends React.Component{
  constructor(props){
    super(props);
    this.state ={
      zone_id : this.props.id,
      records:[],
      addRecordMode:false,
      editRecordMode:false,
      editRecordData:null
    };
    this.backButton = this.backButton.bind(this);
    this.deleteResourceRecord = this.deleteResourceRecord.bind(this);
    this.editResourceRecord = this.editResourceRecord.bind(this);
  }

  async getZoneRecords() {
    let response = await fetch("http://127.0.0.1:5000/api/zone-records/?id="+this.props.id,{
    method: "get",
    headers: {"api-key":process.env.REACT_APP_API_KEY}
    })
    if (response.ok){
      let records = await response.json();
      console.log("zone records received: ", records)
      let recordSet = records.map(record =>
        <ResourceRecordRow key={record.id} record_data={record} deleteFunc={this.deleteResourceRecord} editFunc={this.editResourceRecord}/>
      );
      this.setState({
        records: recordSet
      });
    }
    else{
      alert(response.text);
    }
  }

  deleteResourceRecord(id){
    fetch("http://127.0.0.1:5000/api/zone-records/?id="+id ,{
    method:"DELETE",
    headers:{"api-key":process.env.REACT_APP_API_KEY}
  }).then(response =>response.json())
  .then(json => {
    if (json["error"]){
      alert("ERROR: " +json["error"])
    }
    else{
      alert("Resource record Deleted");
      this.getZoneRecords();
    }
  })
  .catch(error => alert("ERROR: " +error))
  }

  backButton(){
    this.setState({
      addRecordMode:false,
      editRecordMode:false,
      editRecordData: null,
      records: []
    });
    this.getZoneRecords();
  }

  componentDidMount(){
    this.getZoneRecords();
  }

  editResourceRecord(recordData){
    this.setState({
      addRecordMode:false,
      editRecordMode:true,
      editRecordData:recordData
    })
  }

  render(){
    if (this.state.addRecordMode){ 
      //return the add resource record form if the flag is set
      return(
        <AddResourceRecordForm zoneId={this.state.zone_id} backFunc={this.backButton} />
      )
    }
    else if(this.state.editRecordMode){
      return(
        <EditResourceRecordForm recordData={this.state.editRecordData} backFunc={this.backButton} />
      )
    }
    else{
      return(
        <div>
        <h1>RRset for zone {this.props.name} </h1>
        < table class="table table-hover">
          <thead>
            <tr>
              <td>Name</td>
              <td>Record Type</td>
              <td>Value</td>
              <td>TTL</td>
              <td>Actions</td>
            </tr>
              {this.state.records}
          </thead>
        </table>
        <button class="btn btn-success" onClick={() => this.setState({addRecordMode:true})}>
          Add a new Resource Record
        </button>
        </div>
      )
    }
  }
}

class ResourceRecordRow extends React.Component{
  constructor(props) {
    super(props);
    this.state={
      id:this.props.record_data.id,
      name:this.props.record_data.name,
      type:this.props.record_data.type,
      content:this.props.record_data.content,
      ttl:this.props.record_data.ttl,
      priority:this.props.record_data.priority,
    }
    this.confirmDelete = this.confirmDelete.bind(this);
    this.editRecordHandler = this.editRecordHandler.bind(this);
  }

  confirmDelete(){
    confirmAlert({
        title: "Confirm: This option is non reversible ",
        message: "Are you sure you want to delete "+ this.props.record_data.type+ " resource record: "+this.props.record_data.name,
        buttons:[
            {
                label: "Confirm Deletion",
                onClick:() => this.props.deleteFunc(this.props.record_data.id)
            },
            {
                label: "Cancel",
                onClick:""
            }
        ] 
    });
}

  editRecordHandler(){
    this.props.editFunc(this.props.record_data);
  }

  render(){
    return(
      <tr>
        <td>{this.state.name}</td>
        <td>{this.state.type}</td>
        <td>{this.state.content}</td>
        <td>{this.state.ttl}</td>
        <td>
          {this.state.type!=="SOA" && <button class="btn btn-success" onClick={this.editRecordHandler}>Edit Record</button>} 
          {this.state.type!=="SOA" && <button class="btn btn-danger" onClick={this.confirmDelete}>Delete Record</button>}
        </td>
      </tr>
    )
  }
}

export default ZoneRecordsTable