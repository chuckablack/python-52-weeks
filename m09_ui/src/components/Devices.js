import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import Grid from "@material-ui/core/Grid";
import 'typeface-roboto'
import CheckCircleIcon from "@material-ui/icons/CheckCircle";
import {green, red} from "@material-ui/core/colors";
import CancelIcon from "@material-ui/icons/Cancel";
import MaterialTable from "material-table";

class Devices extends Component {

    constructor(props) {
        super(props);
        this.state = {
            devices: [],
            dashboard: props.dashboard,
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
        };
    }

    countdown() {
        this.setState({countdownValue: this.state.countdownValue-1})
        if (this.state.countdownValue === 0) {
            this.fetchDevices()
        }
    }

    fetchDevices() {

        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/devices'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                console.log(data)
                this.setState({devices: data})
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            })
            .catch((e) => {
                console.log(e)
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            });
    }

    componentDidMount() {
        this.fetchDevices(false)
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    render() {

        const {devices} = this.state;

        return (
            <div className="container" style={{maxWidth: "100%"}}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Devices Table</h2>
                    <h6>Time until refresh: {this.state.countdownValue} seconds</h6>
                    <Button variant="contained" onClick={() => {
                        this.fetchDevices()
                    }}>Refresh Devices</Button>
                </Grid>
                <MaterialTable
                    title="Device Status"
                    columns={[
                        {
                            width: null,
                            title: 'Status',
                            render: rowData =>
                                rowData.availability ?
                                    <CheckCircleIcon style={{color: green[500]}}/>
                                    : <CancelIcon style={{color: red[500]}}/>,
                            customSort: (a, b) => {
                                if( a.availability && !b.availability ) return 1;
                                else if (a.availability === b.availability ) return 0
                                else return -1;
                            }
                        },
                        {   title: 'Name',
                            field: 'name',
                            defaultSort: 'asc',
                            customSort: (a, b) => {
                                if( a.name.toUpperCase() > b.name.toUpperCase() ) return 1;
                                else if( a.name.toUpperCase() < b.name.toUpperCase() ) return -1;
                                else return 0;
                            }
                        },
                        { title: 'Hostname', field: 'hostname', defaultSort: 'asc' },
                        { title: 'Vendor:OS', render: rowData => rowData.vendor + ":" + rowData.os},
                        { title: 'IP Address', field: 'ip_address' },
                        { title: 'Model', field: 'model' },
                        { title: 'Version', field: 'os_version' },
                        { title: 'Rsp Time', render: rowData =>  rowData.response_time.toFixed(3) },
                        { title: 'Last Checked', field: 'last_heard' },
                    ]}
                    data={  Object.values(devices) }
                    options={{
                        sorting: true,
                        padding: "dense",
                        pageSize: 10,
                        rowStyle: (rowData) => {
                            if(!rowData.availability) {
                                return {color: 'red'};
                            }
                            else {
                                return {color: 'chartreuse'}
                            }
                        }
                    }}
                />
            </div>
        );
    }
}

export default Devices;
