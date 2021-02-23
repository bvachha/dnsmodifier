import React from "react";
import Table from "react-bootstrap/Table"
import { confirmAlert } from "react-confirm-alert"
import 'react-confirm-alert/src/react-confirm-alert.css'


class ZoneTable extends React.Component{
  
    constructor(props){
      super(props);
      this.state = {
        zone_rows: [],
        zones: []
      };
      this.deleteZone = this.deleteZone.bind(this);
      this.editZone = this.editZone.bind(this);
    }

    async getZones(){
      const api_key = process.env.REACT_APP_API_KEY;
      let response = await fetch('http://127.0.0.1:5000/api/zones/',{
       method: "get",
       headers:{
       "api-key":api_key
       }
      });
      if (response.ok){
        let response_json = await response.json();
        return response_json;
      }
    }

    editZone(id,name){
      this.props.onZoneEdit(id,name);
    }

    async deleteZone(id,name){
        fetch("http://127.0.0.1:5000/api/zones/?id="+id,
        {method: "DELETE",
        headers:{"api-key":process.env.REACT_APP_API_KEY}
        })
        .then(response => response.json())
        .then(json=>{
            if (json["error"]){
                alert("Something went wrong");
            }
            else{
                alert("Record for zone :" + name + " deleted");
            }
        })
        .catch(error =>{
            alert("Error: "+error);
        })
        //remove the deleted row from the array containing the rows
        let records = this.state.zone_rows.slice()
        let new_records = records.filter(function(value, index, arr){
            return value.props.id !== id;
        })
        //update the state to remove the deleted row
        this.setState({ 
            zone_rows: new_records
        });
    }

    componentDidMount(){
      this.getZones().then(response => {      
        this.setState({zones: response}, () => {
          const rows = this.state.zones.map((zone)=>
          <ZoneRow name={zone.name} key={zone.id} id={zone.id} delete_func={this.deleteZone} edit_func={this.editZone} />
          );
          this.setState({zone_rows: rows});
        }
        );
      });     
    }
    
    render(){
      return(
        <div>
          <Table striped bordered hover>
            <thead>
                <tr>
                  <th colWidth="70%">Zone name</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {this.state.zone_rows}
              </tbody>
          </Table>
        </div>
      );
    }
  }
  



  class ZoneRow extends React.Component{
    constructor(props){
        super(props);
        this.confirmDelete = this.confirmDelete.bind(this);
        this.zone_delete = this.zone_delete.bind(this);
        this.zone_edit = this.zone_edit.bind(this);
    }  

    zone_delete(){
        this.props.delete_func(this.props.id,this.props.name);
    }

    zone_edit(){
      
        this.props.edit_func(this.props.id, this.props.name);
    }


    confirmDelete(){
        confirmAlert({
            title: "Confirm: This option is non reversible ",
            message: "Are you sure you want to delete zone: "+this.props.name,
            buttons:[
                {
                    label: "Confirm Deletion",
                    onClick:this.zone_delete
                },
                {
                    label: "Cancel",
                    onClick:""
                }
            ] 
        });
    }

    render(){
        return(
        <tr>
            <td>{this.props.name}</td>
            <td>
              <div class="d-grid gap-2 d-md-block">
                <button type="button" className="btn btn-outline-primary" id="edit-zone" onClick={this.zone_edit}>Edit Zone Records</button>
                <button type="button" className="btn btn-outline-danger" id="delete-zone" onClick={this.confirmDelete}>Delete Zone</button>
              </div> 
            </td>
        </tr>
        );
        }
  }
  
  export default ZoneTable