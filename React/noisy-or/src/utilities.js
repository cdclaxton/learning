// Round a probability to two decimal places.
export const formatProbability = (prob) => {
  return Math.round(prob * 100) / 100
}