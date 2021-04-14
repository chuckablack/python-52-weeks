import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import Grid from "@material-ui/core/Grid";
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import CancelIcon from '@material-ui/icons/Cancel';
import {green, red} from '@material-ui/core/colors';
import MaterialTable from "material-table";
import PolicyRoundedIcon from '@material-ui/icons/PolicyRounded'
import Dialog from '@material-ui/core/Dialog'
import DialogTitle from '@material-ui/core/DialogTitle'
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";

class Hosts extends Component {

    constructor(props) {
        super(props);
        this.state = {
            hosts: [],
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
            openExtendedPortScanDialog: false,
            portScanHost: '',
            portScanResults: '',
            extendedPortScanResults: '',
            token: '',
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

    initiateExtendedPortScan(hostname) {

        this.setState({extendedPortScanResults: {result: "initiating scan ..."}})
        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/scan?target=' + hostname
        const requestOptions = { method: 'POST'}
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({token: data.token})
                this.fetchExtendedPortScanResults(hostname)
                console.log(this.state.extendedPortScanResults)
            })
            .catch(console.log)
    }

    fetchExtendedPortScanResults(hostname) {
       this.setState({extendedPortScanResults: {result: "retrieving scan results ..."}})
        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/scan?target=' + hostname + '&token=' + this.state.token
        const requestOptions = { method: 'GET'}
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({extendedPortScanResults: data})
                console.log(this.state.extendedPortScanResults)
            })
            .catch(console.log)

    }

    componentDidMount() {
        this.fetchHosts()
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    renderExtendedPortScanDialog(hostId, ip) {
        this.initiateExtendedPortScan(hostId)
        this.setState({openExtendedPortScanDialog: true, portScanHost: ip})
    }

    handleCloseExtendedPortScanDialog(parent) {
        parent.setState({openExtendedPortScanDialog: false})
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
                    title="Discovered Hosts with Availability, Open TCP Ports"
                    columns={[
                        {
                            title: 'Status',
                            render: rowData =>
                                rowData.availability ?
                                    <CheckCircleIcon style={{color: green}}/>
                                    : <CancelIcon style={{color: red}}/>,
                            customSort: (a, b) => {
                                if( a.availability && !b.availability ) return 1;
                                else if (a.availability === b.availability ) return 0
                                else return -1;
                            }
                        },
                        {   title: 'Hostname',
                            field: 'hostname',
                            customSort: (a, b) => {
                                if( a.hostname.toUpperCase() > b.hostname.toUpperCase() ) return 1;
                                else if( a.hostname.toUpperCase() < b.hostname.toUpperCase() ) return -1;
                                else return 0;
                            }
                        },
                        { title: 'IP Address', field: 'ip_address', defaultSort: 'asc' },
                        { title: 'MAC Address', field: 'mac_address' },
                        { title: 'Rsp Time', field: 'response_time', type: 'numeric' }, 
                        { title: 'Last Heard', field: 'last_heard' },
                        { title: 'Open Ports', field: 'open_tcp_ports'}
                    ]}
                    data={ Object.values(hosts) }
                    options={{
                        sorting: true,
                        padding: "dense",
                        pageSize: 10,
                        rowStyle: (rowData) => {
                            if(!rowData.availability) {
                                return {color: 'red'};
                            }
                            else if(('open_tcp_ports' in rowData) && (rowData.open_tcp_ports.length > 2)) {
                                return {color: 'yellow'}
                            }
                            else {
                                return {color: 'chartreuse'}
                            }
                        },
                        cellStyle: { fontSize: 14, }
                    }}
                    actions={[
                        {
                            icon: PolicyRoundedIcon,
                            tooltip: 'Extended Scan for open ports',
                            onClick: (event, rowData) => {
                                this.renderExtendedPortScanDialog(rowData.hostname)
                            }
                        },
                     ]}

                />
                <Dialog
                    open={this.state.openExtendedPortScanDialog}
                    maxWidth="lg"
                >
                    <DialogTitle>Extended Port Scan Results: {this.state.portScanHost}</DialogTitle>
                    <DialogContent>
                        <b>Output from extended scan:</b><br />
                        Result: {this.state.extendedPortScanResults.result}<br />
                        Extended scan results:
                        <br /><br />
                        <pre style={{color: 'white'}}>
                            {this.state.extendedPortScanResults.scan_output}
                        </pre>
                        <br /><br />
                        <b>NOTE:</b><br />
                        Depending on the host, scanning may take up to a few minutes to complete
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => this.handleCloseExtendedPortScanDialog(this)}>
                            Close
                        </Button>
                    </DialogActions>
                </Dialog>
            </div>
        );
    }
}

export default Hosts;
