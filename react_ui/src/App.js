// import logo from './logo.svg';
import "./App.css";
import * as React from "react";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import TextareaAutosize from "@mui/material/TextareaAutosize";
import axios from "axios";

import CanvasJSReact from "./assets/canvasjs.react";
var CanvasJSChart = CanvasJSReact.CanvasJSChart;

function App() {
  const [script, setScript] = React.useState("");
  const [output, setOutput] = React.useState({});

  const updateOutput = async () => {
    axios
      .post("/", {
        script: script,
      })
      .then(function (response) {
        // handle success
        // console.log();
        if (response.data.status === true) {
          let datapoints = {};
          // console.log(response.data.OUT)
          response.data.OUT.forEach((OUT) => {
            let outvars = [];
            outvars.push({ label: `OUT_${OUT.VAR}`, y: [OUT.MIN, OUT.MAX] });
            OUT.IN.forEach((IN) => {
              outvars.push({ label: `IN_${IN.VAR}`, y: [IN.MIN, IN.MAX] });
            });
            datapoints[`OUT_${OUT.VAR}`] = outvars;
            // console.log(outvars);
          });
          setOutput(datapoints);
        }
        // setOutput(response.data);
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      })
      .then(function () {
        // always executed
      });
  };

  return (
    <React.Fragment>
      <header class="App-header">
        <Container
          maxWidth="xl"
          sx={{
            marginTop: 3,
            justifyContent: "center",
            justifyItems: "center",
            alignItems: "center",
            alignContent: "center",
          }}
        >
          <Grid container spacing={1}>
            <Grid item xs={11}>
              <TextareaAutosize
                aria-label="minimum height"
                minRows={3}
                onChange={(event) => {
                  setScript(event.target.value);
                }}
                placeholder="Minimum 3 rows"
                style={{ width: "100%" }}
              />
            </Grid>
            <Grid item xs={1}>
              <Button
                sx={{
                  marginTop: 1,
                  marginLeft: 1,
                  width: "90%",
                  display: "flex",
                  alignItems: "center",
                }}
                onClick={updateOutput}
                variant="contained"
              >
                find
              </Button>
            </Grid>
            {Object.keys(output).map((item) => {
              // console.log(JSON.stringify(output[item]));
              return (
                <Grid key={item} item xs={12}>
                  <CanvasJSChart
                    options={{
                      theme: "dark2",
                      exportEnabled: true,
                      animationEnabled: true,
                      title: {
                        text: `Min & Max for [${item}]`,
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
                          dataPoints: output[item],
                        },
                      ],
                    }}
                  />
                </Grid>
              );
            })}
          </Grid>
        </Container>
      </header>
    </React.Fragment>
  );
}

export default App;
