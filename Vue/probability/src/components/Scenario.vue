<script lang="js"></script>

<template>
  <div class="scenario">
    <div class="scenario-detail">
      <!-- Button to delete the scenario -->
      <button class="delete-scenario">&times;</button>

      <!-- Text box for the scenario name -->
      <input class="scenario-name" type="text" placeholder="Scenario name" />

      <!-- Table for the probability distribution -->
      <div class="scenario-prob-table">
        <!-- Header row -->
        <div>Value</div>
        <div>Probability</div>
        <div></div>
        <input type="text" />
        <input type="text" />
        <button class="delete-probability-row">&times;</button>
        <input type="text" />
        <input type="text" />
        <button class="delete-probability-row">&times;</button>
        <input type="text" />
        <input type="text" />
        <button class="delete-probability-row">&times;</button>
      </div>

      <!-- Buttons to add and normalise probabilities -->
      <div class="probability-buttons">
        <button class="add-probability-row">+</button>
        <button class="normalise-probabilities">Normalise</button>
      </div>
    </div>

    <!-- Probability of the scenario occurring -->
    <div class="scenario-prob-div">
      <p>p =</p>
      <input class="scenario-prob" type="text" placeholder="1.0" />
    </div>
  </div>
</template>
