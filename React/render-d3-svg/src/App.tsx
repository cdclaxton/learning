import { useEffect, useMemo, useRef, useState } from "react";
import * as d3 from "d3";
import { useInterval } from "usehooks-ts";
import { animated, useSpring } from "@react-spring/web";

const Svg = () => {
  return (
    <svg style={{
      border: "2px solid gold"
    }} />
  );
}

const Circle = () => {
  const ref = useRef(null);

  useEffect(() => {
    const svgElement = d3.select(ref.current);
    svgElement.append("circle")
      .attr("cx", 150)
      .attr("cy", 70)
      .attr("r", 50)
    }, []);
  
  return (
    <svg ref={ref} />
  )
}

const Circle2 = () => {
  return (
    <svg>
      <circle cx="150" cy="77" r="40" />
    </svg>
  )
}

const generateDataset = () => {
  return Array(10).fill(0).map(() => ([
    Math.random() * 80 + 10,
    Math.random() * 35 + 10,
  ]))
}

const Circles = () => {
  const [dataset, setDataset] = useState(generateDataset());
  const ref = useRef(null);

  useEffect(() => {
    const svgElement = d3.select(ref.current);
    svgElement.selectAll("circle")
      .data(dataset)
      .join("circle")
      .attr("cx", d => d[0])
      .attr("cy", d => d[1])
      .attr("r", 3)
  }, [dataset])  

  useInterval(() => {
    const newDataset = generateDataset();
    setDataset(newDataset);
  }, 2000);

  return (
    <svg viewBox="0 0 100 50" ref={ref} />
  )
}

const generateCircles2 = () => {
  const margin = 10;
  const width = 300;
  const height = 150;
  return Array(6).
    map((_,index: number) => [margin + ((width - 2*margin)/7)*index, height/2])
}

const generateCircles = () => {
  const result =  [1,2,3,4,5,6];

  for (let i=0; i<result.length; i++) {
    if (Math.random() > 0.5) {
      result[i] = -1;
    } 
  }

  return result.filter(value => value !== -1);
}

const AnimatedCircles = () => {
  const [visibleCircles, setVisibleCircles] = useState(generateCircles());
  const ref = useRef(null);

  useInterval(() => {
    setVisibleCircles(generateCircles());
  }, 2000);

  useEffect(() => {
    const svgElement = d3.select(ref.current);
    svgElement.selectAll("circle")
      .data(visibleCircles, d => d)
      .join(
        enter => (
          enter.append("circle")
            .attr("cx", d => d * 15 + 10)
            .attr("cy", 10)
            .attr("r", 0)
            .attr("fill", "cornflowerblue")
          .call(enter => (
            enter.transition().duration(1200)
              .attr("cy", 10)
              .attr("r", 6)
              .style("opacity", 1)
          ))
        ),
        update => (
          update.attr("fill", "lightgrey")
        ),
        exit => (
          exit.attr("fill", "tomato")
            .call(exit => (
              exit.transition().duration(1200)
                .attr("r", 0)
                .style("opacity", 0)
                .remove()
            ))
        ),
      )
  }, [visibleCircles]); 

  return (
    <svg viewBox="0 0 100 20" ref={ref} />
  )
}

const AnimatedCircle = ({index, isShowing}: {index: number, isShowing: boolean}) => {
  const wasShowing = useRef(false);

  useEffect(() => {
    wasShowing.current = isShowing;
  }, [isShowing]);

  const style = useSpring({
    config: {
      duration: 1200
    },
    r: isShowing ? 6 : 0,
    opacity: isShowing ? 1 : 0,
  })

  return (
    <animated.circle {...style}
      cx = {index*15 + 10}
      cy = "10"
      fill = {
        !isShowing          ? "tomato" :
        !wasShowing.current ? "cornflowerblue" :
                              "lightgrey"  
      }
    />
  )
}

const AnimatedCircles2 = () => {
  const [visibleCircles, setVisibleCircles] = useState(generateCircles());
  const allCircles = Array(6).fill(0).map((_, index) => index);

  useInterval(() => {
    setVisibleCircles(generateCircles());
  }, 2000);

  return (
    <svg viewBox="0 0 100 20">
      {allCircles.map(d => (
        <AnimatedCircle key={d} index={d} isShowing={visibleCircles.includes(d)} />
      ))}
    </svg>
  )
}

// Create an x-axis using d3
const Axis = () => {
  const ref = useRef(null);

  useEffect(() => {
    // Values 0 to 100 at 10px to 290px
    const xScale = d3.scaleLinear()
      .domain([0, 100])
      .range([10, 290]);

    const svgElement = d3.select(ref.current);
    const axisGenerator = d3.axisBottom(xScale);
    svgElement.append("g").call(axisGenerator);
  }, []);

  return (
    <svg ref={ref} />
  )
}

const Axis2 = () => {
  const ticks = useMemo(() => {
    const xScale = d3.scaleLinear()
      .domain([0, 100])
      .range([10, 290]);

    return xScale.ticks().map(value => ({
      value, 
      xOffset: xScale(value)
    }))
  }, []);

  return (
    <svg>
      <path d="M 9.5 0.5 H 290.5" stroke="currentColor" />
      {ticks.map(({value, xOffset}) => (
        <g key={value} transform={`translate(${xOffset}, 0)`}>
          <line y2="6" stroke="currentColor" />
          <text key={value} style={{
            fontSize: "10px",
            textAnchor: "middle",
            transform: "translateY(20px)"
          }}>{ value }</text>
        </g>
      ))}
      
    </svg>
  )
};

type BarGraphDataElement = {
  label: string;
  value: number;
}

const randomValueInRange = (minValue: number, maxValue: number): number => {
  return Math.random() * (maxValue - minValue) + minValue;
}

const generateCategoricalDataset = (labels: string[], minValue: number,
  maxValue: number
): BarGraphDataElement[] => {

  return labels.map((label) => ({
    label: label,
    value: randomValueInRange(minValue, maxValue)
  }))
};

const maxValue = (dataset: BarGraphDataElement[]): number => {
  return dataset.map(element => element.value).sort((a,b) => b-a)[0];
}

type ChartDimensions = {
  width: number;
  height: number;
  marginTop: number;
  marginRight: number;
  marginLeft: number;
  marginBottom: number;
}

const chartSettings: ChartDimensions = {
  width: 400,
  height: 200,
  marginTop: 10,
  marginRight: 40,
  marginLeft: 40,
  marginBottom: 50,
}

const BarGraph = ({dataset}: {dataset: BarGraphDataElement[]}) => {

  const [ref, dms] = useChartDimensions(chartSettings);

  const width = Math.max(dms.width - dms.marginLeft - dms.marginRight, 0);
  const height = Math.max(dms.height - dms.marginTop - dms.marginBottom, 0);

  useEffect(() => {
    
    const svgElement = d3.select(ref.current);

    const svgElement2 = svgElement
      .append("svg")
        .attr("width", `${dms.width}`)
        .attr("height", `${dms.height}`)
      .append("g")
        .attr("transform", `translate(${dms.marginLeft}, ${dms.marginTop})`)

    // x-axis
    const xScale = d3.scaleBand()
      .domain(dataset.map(element => element.label))
      .range([0, width])
      .padding(0.2);

    svgElement2.append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(d3.axisBottom(xScale))
      .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end")    

    // y-axis
    const yScale = d3.scaleLinear()
      .domain([0, Math.round(maxValue(dataset)*1.1)])
      .range([height, 0])

    svgElement2.append("g")
      .call(d3.axisLeft(yScale));

    // Add the bars
    svgElement2.selectAll("mybar")
      .data(dataset)
      .enter()
      .append("rect")
        .attr("x", d => xScale(d.label))
        .attr("y", d => yScale(d.value))
        .attr("width", xScale.bandwidth())
        .attr("height", d => height - yScale(d.value))
        .attr("fill", "#69b3a2")

  }, []);

  return (
    <svg
      viewBox={`0 0 ${dms.width} ${dms.height}`}
      ref={ref} />
  )
}

const combineChartDimensions = (dimensions: ChartDimensions): ChartDimensions => {
  return {
    ...dimensions,
    marginTop: dimensions.marginTop || 10,
    marginRight: dimensions.marginRight || 10,
    marginBottom: dimensions.marginBottom || 40,
    marginLeft: dimensions.marginLeft || 75,
  };
};

const useChartDimensions = (passedSettings: ChartDimensions) => {

  const ref = useRef(null);
  const dimensions = combineChartDimensions(passedSettings);

  const [width, setWidth] = useState(0);
  const [height, setHeight] = useState(0);

  useEffect(() => {

    const element = ref.current;
    const resizeObserver = new ResizeObserver(
      entries => {
        if (!Array.isArray(entries) || !entries.length) {
          return null;
        }

        const entry = entries[0];

        if (width != entry.contentRect.width) {
          setWidth(entry.contentRect.width);
        }
        if (height != entry.contentRect.height) {
          setHeight(entry.contentRect.height);
        }
      }
    )

    resizeObserver.observe(element);

    return () => resizeObserver.unobserve(element);
  }, []);

  const newSettings: ChartDimensions = combineChartDimensions({
    ...dimensions,
    width: dimensions.width || width,
    height: dimensions.height || height,
  })

  return [ref, newSettings];
};

const App = () => {
  const daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
  const weekDataset = generateCategoricalDataset(daysOfWeek, 0, 10);

  const timesOfDay = Array(24).fill(1).map((_,index) => `${index}`)
  const timesOfDayDataset = generateCategoricalDataset(timesOfDay, 0, 40);

  return (
    <>
      <h1>Creating SVG elements</h1>
    {/* <Svg />
    <Circle />
    <Circle2 />
    <Circles />
    <AnimatedCircles2 />
    <Axis />
    <Axis2 /> */}

      <div className="bar-graphs">
        <div className="bar-graph">
          <BarGraph dataset={weekDataset} />
        </div>
        <div className="bar-graph">
          <BarGraph dataset={timesOfDayDataset} />
        </div>
      </div>
    </>
  )
}

export default App;