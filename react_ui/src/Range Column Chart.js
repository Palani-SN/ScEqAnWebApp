import React, { Component } from "react";
import CanvasJSReact from "./assets/canvasjs.react";
var CanvasJSChart = CanvasJSReact.CanvasJSChart;

class RangeColumnChart extends Component {
  render() {
    const options = {
      theme: "dark2",
      exportEnabled: true,
      animationEnabled: true,
      title: {
        text: "Min & Max for Output Variable P",
      },
      axisX: {},
      axisY: {
        title: "Worst Case Ranges",
        gridThickness: 0,
      },
      data: [
        {
          type: "rangeColumn",
          indexLabel: "{y[#index]}",
          toolTipContent:
            " <strong> Var: {label} </strong></br> Max: {y[1]} <br/> Min: {y[0]} ",
          dataPoints: [
            { label: "Var1", y: [19, 26] },
            { label: "Var2", y: [19, 26] },
            { label: "Var3", y: [18, 25] },
            { label: "Var4", y: [15, 23] },
            { label: "Var5", y: [12, 20] },
            { label: "Var6", y: [10, 18] },
            { label: "Var7", y: [8, 17] },
            { label: "Var8", y: [9, 18] },
            { label: "Var9", y: [12, 20] },
            { label: "Var10", y: [14, 22] },
            { label: "Var11", y: [16, 24] },
            { label: "Var12", y: [18, 26] },
          ],
        },
      ],
    };

    return (
      <div>
        <CanvasJSChart
          options={options}
          /* onRef={ref => this.chart = ref} */
        />
        {/*You can get reference to the chart instance as shown above using onRef. This allows you to access all chart properties and methods*/}
      </div>
    );
  }
}

export default RangeColumnChart;
