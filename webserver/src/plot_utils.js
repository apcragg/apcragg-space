export class PercentileBounds {
    /**
     * Creates an empty array to hold the measurements
     * @param {number} maxMeasurements - The maximum number of measurements to store
     */
    constructor(maxMeasurements) {
      this.measurements = [];
      this.maxMeasurements = maxMeasurements;
    }

    /**
     * Adds a measurement, which is a constant length vector, to the class
     * @param {Array} measurement
     */
    addMeasurement(measurement) {
      this.measurements.push(measurement);
      if (this.measurements.length > this.maxMeasurements) {
        this.measurements.shift();
      }
    }

    /**
     * Returns the bounds of a given percentile of the most recent measurements
     * @param {number} percentile - The percentile to calculate the bounds for, it should be a value between 0 and 1
     * @returns {Array} bounds - an array of bounds, where each bound is an array of [lowerBound, upperBound]
     */
    getBounds(percentile = 0.95) {
      const recentMeasurements = this.measurements.slice(-this.maxMeasurements);
      let bounds = []
      for(let i=0; i< recentMeasurements[0].length; i++){
          let column = recentMeasurements.map(row => row[i])
          column.sort((a, b) => a - b);
          const lowerBound = column[Math.floor(column.length * (1-percentile))];
          const upperBound = column[Math.floor(column.length * percentile)];
          bounds.push([lowerBound, upperBound]);
      }
      return bounds;
    }
  }

/**
 * Calculates the element-wise maximum of two arrays
 * @param {*} a - Arraylike
 * @param {*} b - Arraylike
 * @returns Array with element-wise max of {a, b}
 */
export function elementwiseMax(a, b) {
    if (!Array.isArray(a) || !Array.isArray(b)) {
        throw new Error("Both inputs must be an array.");
    }
    if (a.length !== b.length) {
        throw new Error("Both inputs must have the same length.");
    }
    return a.map((val, idx) => Math.max(val, b[idx]));
}
