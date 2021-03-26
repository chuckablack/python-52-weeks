import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import Grid from "@material-ui/core/Grid";
import 'typeface-roboto'
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import CancelIcon from '@material-ui/icons/Cancel';
import {green, red} from '@material-ui/core/colors';
import MaterialTable from "material-table";

class Hosts extends Component {

    constructor(props) {
        super(props);
        this.state = {
            hosts: [],
            dashboard: props.dashboard,
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
       };
    }

    countdown() {
        this.setState({countdownValue: this.state.countdownValue-1})
        if (this.state.countdownValue === 0) {
            this.fetchHosts()
        }
    }

    fetchHosts() {

        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/hosts'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                console.log(data)
                this.setState({hosts: data})
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            })
            .catch((e) => {
                console.log(e)
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            });
    }

    componentDidMount() {
        this.fetchHosts()
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    render() {

        const {hosts} = this.state;

        return (

            <div className="container" style={{maxWidth: "100%"}}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Hosts Table</h2>
                    <h6>Time until refresh: {this.state.countdownValue} seconds</h6>
                    <Button variant="contained" onClick={() => {
                        this.fetchHosts()
                    }}>Refresh Hosts</Button>
                </Grid>
                <MaterialTable
                    title="Discovered Hosts with Availability and Response Time"
                    columns={[
                        {
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
                        {   title: 'Hostname',
                            field: 'hostname',
                            customSort: (a, b) => {
                                if( a.name.toUpperCase() > b.name.toUpperCase() ) return 1;
                                else if( a.name.toUpperCase() < b.name.toUpperCase() ) return -1;
                                else return 0;
                            }
                        },
                        { title: 'IP Address', field: 'ip_address', defaultSort: 'asc' },
                        { title: 'MAC Address', field: 'mac_address' },
                        { title: 'Rsp Time', render: rowData =>  rowData.response_time.toFixed(3) },
                        { title: 'Last Heard', field: 'last_heard' },
                    ]}
                    data={ Object.values(hosts) }
                    options={{
                        sorting: true,
                        padding: "dense",
                        pageSize: 10,
                    }}

                />
            </div>
        );
    }
}

export default Hosts;
