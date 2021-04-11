import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import Grid from "@material-ui/core/Grid";
// import 'typeface-roboto'
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import CancelIcon from '@material-ui/icons/Cancel';
import {green, red} from '@material-ui/core/colors';
import MaterialTable from "material-table";

class Services extends Component {

    constructor(props) {
        super(props);
        this.state = {
            services: [],
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
        };
    }

    countdown() {
        this.setState({countdownValue: this.state.countdownValue-1})
        if (this.state.countdownValue === 0) {
            this.fetchServices()
        }
    }

    fetchServices() {

        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/services'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                this.setState({services: data})
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})

            })
            .catch((e) => {
                console.log(e)
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            });
    }

    componentDidMount() {
        this.fetchServices()
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    render() {

        const {services} = this.state;

        return (
            <div className="container" style={{maxWidth: "100%"}}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Services Table</h2>
                    <h6>Time until refresh: {this.state.countdownValue} seconds</h6>
                    <Button variant="contained" onClick={() => {
                        this.fetchServices()
                    }}>Refresh Services</Button>
                </Grid>
                <MaterialTable
                    title="Services with Availability, Response Time, SLA Violations"
                    columns={[
                        {
                            title: 'Availability',
                            field: 'availability',
                            headerStyle: {textAlign: 'right'},
                            cellStyle: {textAlign: 'center'},
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
                        { title: 'Type', field: 'type' },
                        { title: 'Target', field: 'target' },
                        { title: 'Data', field: 'data' },
                        { title: 'Rsp Time', render: rowData =>  rowData.response_time.toFixed(3) },
                        { title: 'Last Heard', field: 'last_heard' },
                    ]}
                    data={ Object.values(services) }
                    options={{
                        sorting: true,
                        padding: "dense",
                        pageSize: 10,
                        rowStyle: (rowData) => {
                            if(!rowData.availability) {
                                return {color: 'red'};
                            }
                            else if(rowData.response_time > rowData.sla_response_time) {
                                return {color: 'Magenta'}
                            }
                            else {
                                return {color: 'chartreuse'}
                            }
                        },
                        cellStyle: { fontSize: 14, }
                    }}
                />
            </div>
        );
    }
}

export default Services;
