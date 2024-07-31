/** @odoo-module */

import {loadJS} from "@web/core/assets";
const {Component, onWillStart, useRef, onMounted, useEffect} = owl;
// import {useEffect} from "@odoo/owl";

export class ChartRenderer extends Component {
  setup() {
    this.chartRef = useRef("chart");
    this.chartInstance = null;

    onWillStart(async () => {
      await loadJS(
        "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"
      );
    });
    onMounted(() => this.renderChart());
    useEffect(
      () => {
        this.updateCharts();
      },
      () => [this.props]
    );
  }

  renderChart() {
    const ctx = this.chartRef.el;

    if (this.props.type === "line") {
      this.chartInstance = new Chart(ctx, {
        type: this.props.type,
        data: {
          labels: this.props.chartData,
          datasets: this.props.dataSets,
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            mode: "index",
            intersect: false,
          },
          stacked: false,
          plugins: {
            title: {
              display: true,
              position: "bottom",
              text: this.props.title,
            },
          },
          scales: {
            y: {
              type: "linear",
              display: true,
              position: "left",
            },
          },
        },
      });
    } else if (this.props.type === "pie") {
      this.chartInstance = new Chart(ctx, {
        type: "pie",
        data: {
          labels: ["Offical site", "Channel manager", "Movo PMS", "Others"],
          datasets: [
            {
              label: "My First Dataset",
              data: [200, 50, 100, 150],
              backgroundColor: ["#72BEF1", "#F86464", "#8FC198", "#C1D69A"],
              hoverOffset: 4,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });
    } else if (this.props.type === "bar") {
      this.chartInstance = new Chart(ctx, {
        type: "bar",
        data: {
          labels: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль"],
          datasets: [
            {
              label: "Официальный сайт",
              backgroundColor: "rgba(255, 99, 132, 0.2)",
              borderColor: "rgba(255, 99, 132, 1)",
              borderWidth: 1,
              data: [8.46, 0, 0, 0, 26.05, 0, 0],
            },
            {
              label: "Channel Manager",
              backgroundColor: "rgba(54, 162, 235, 0.2)",
              borderColor: "rgba(54, 162, 235, 1)",
              borderWidth: 1,
              data: [0, 0, 0, 27.52, 0, 0, 38.3],
            },
            {
              label: "Movo PMS",
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 1,
              data: [91.54, 100, 3.95, 73.95, 73.95, 61.7, 39.8],
            },
            {
              label: "Прочие",
              backgroundColor: "rgba(153, 102, 255, 0.2)",
              borderColor: "rgba(153, 102, 255, 1)",
              borderWidth: 1,
              data: [0, 0, 0, 0, 0, 0, 0],
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              stacked: true,
            },
            y: {
              stacked: true,
              beginAtZero: true,
              max: 100, // Максимум оси y должен быть 100, так как данные в процентах
            },
          },
          plugins: {
            tooltip: {
              callbacks: {
                label: function (context) {
                  let label = context.dataset.label || "";

                  if (label) {
                    label += ": ";
                  }
                  if (context.parsed.y !== null) {
                    label += context.parsed.y + "%";
                  }
                  return label;
                },
              },
            },
          },
        },
      });
    }
  }

  updateCharts() {
    if (this.chartInstance) {
      this.chartInstance.destroy();
    }

    this.renderChart();
  }
}

ChartRenderer.template = "hms_app.ChartRenderer";
