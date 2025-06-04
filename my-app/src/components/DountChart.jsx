import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import { Chart, ArcElement, Tooltip, Legend } from 'chart.js';
import '../styles/DountChart.css';

Chart.register(ArcElement, Tooltip, Legend);

const DonutChart = ({ percentage }) => {

  let color = ''

  if (percentage <= 30){
    color = 'green'
  }else if (percentage > 30 && percentage <= 50){
    color = '#CC9900'
  }else if (percentage > 50 && percentage <= 80){
    color = '#D35400'
  }else{
    color = '#B44D03'
  }

  const data = {
    datasets: [{
      data: [percentage, 100 - percentage],
      backgroundColor: [color, '#e5e7eb'],
      borderWidth: 0
    }]
  };

  const options = {
    cutout: '70%',
    responsive: false,
    plugins: {
      tooltip: { enabled: false },
      legend: { display: false }
    }
  };

  return (
    <div className="chart-container">
      <Doughnut data={data} options={options} />
      <div className="center-text" style={{ color }}>{percentage}%</div>
    </div>
  );
};

export default DonutChart;