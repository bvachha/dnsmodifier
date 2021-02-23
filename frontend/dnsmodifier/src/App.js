import React from 'react';
import ZoneTable from "./Zone_table";
import ZoneRecordsTable from "./RecordsTable"
import AddZoneForm from "./AddZoneForm"

class App extends React.Component {
  constructor(props){
    super(props);
    this.state ={
      isEditZoneMode:false,
      zoneIdUnderEdit:null,
      zoneNameUnderEdit: null,
      zoneAddMode:false
    }
    this.showTable = this.showTable.bind(this);
    this.editZone = this.editZone.bind(this);
    this.resetState = this.resetState.bind(this);
  }

  resetState(){
    this.setState({
      isEditZoneMode:false,
      zoneIdUnderEdit:null,
      zoneNameUnderEdit:null,
      zoneAddMode: false
    })
  }

  showTable(){
    if (this.state.isEditZoneMode){
      return(
        <div>
          <ZoneRecordsTable id={this.state.zoneIdUnderEdit} name={this.state.zoneNameUnderEdit} />
        </div>
      )
    }
    else if(this.state.zoneAddMode){
      return(
        <div>
          <AddZoneForm backButton={this.resetState}/>
        </div>
      )
    }
    
    else{
      return(
        <div>
          <ZoneTable onZoneEdit={this.editZone} />
          <button type="button" className="btn btn-outline-success" onClick={()=>{
              this.setState({
                isEditZoneMode:false,
                zoneIdUnderEdit:null,
                zoneNameUnderEdit:null,
                zoneAddMode: true
                })
              }}>
              Add New Zone
            </button>
        </div>
      );
    }
  }

  editZone(zone_id, zone_name){
      this.setState({
        isEditZoneMode:true,
        zoneIdUnderEdit:zone_id,
        zoneNameUnderEdit:zone_name,
        zoneAddMode:false
      });
  }

  render() {
    return (
      <div className="App">
        <Title />
        {this.showTable()}
      </div>
    );
  }
}



function Title(){
  return (
    <h1> DNS Management Console </h1>
  );
}

export default App;
