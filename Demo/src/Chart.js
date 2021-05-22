import React from 'react';
import ReactApexChart from 'react-apexcharts';

class ApexChart extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            series: [{
                data: []
            }],
            options: {
                chart: {
                    height: 350,
                    type: 'line',
                    id: 'areachart-2'
                },
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    curve: 'straight'
                },
                grid: {
                    padding: {
                        right: 30,
                        left: 20
                    }
                },
                title: {
                    text: 'Chart',
                    align: 'left'
                },
                xaxis: {
                    type: 'datetime',
                },
            },


        };
    }

    static getDerivedStateFromProps = (props, state) => {
        let series = [{ data: props.data }];
        return { series };
    }

    render() {
        return (
            <div id="chart">
                <ReactApexChart options={this.state.options} series={this.state.series} type="line" height={350} />
            </div>
        );
    }
}

export default ApexChart;