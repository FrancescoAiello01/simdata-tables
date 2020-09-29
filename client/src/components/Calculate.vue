<template>
  <div>
    <form class='' method='post' @submit.prevent='postNow'>
      Air Pressure
      <input type='text' air_pressure='' value='' v-model='air_pressure' /> <br />
      Airport Elevation
      <input type='text' airport_elevation='' value='' v-model='airport_elevation' /> <br />
      Outside Air Temperature
      <input type='text' outside_air_temp='' value='' v-model='outside_air_temp' /> <br />
      Runway Length
      <input type='text' runway_length_uncorrected='' value=''
      v-model='runway_length_uncorrected' />
      <br />
      Head Wind
      <input type='text' head_wind='' value='' v-model='head_wind' /> <br />
      Runway Slope Percentage
      <input type='text' slope_percent='' value='' v-model='slope_percent' /> <br />
      Aircraft Weight
      <input type='text' aircraft_weight='' value='' v-model='aircraft_weight' /> <br />
      AP Registration (True / False)
      <input type='text' ap_registration='' value='' v-model='ap_registration' /> <br />
      Air Conditioning
      <input type='text' air_conditioning='' value='' v-model='air_conditioning' /> <br />
      Engine Anti Ice
      <input type='text' engine_anti_ice='' value='' v-model='engine_anti_ice' /> <br />
      Total Anti Ice
      <input type='text' total_anti_ice='' value='' v-model='total_anti_ice' /> <br />
      Operational CG Percentage
      <input type='text' operational_CG_percentage=''
      value='' v-model='operational_CG_percentage' />
      <br />
      <button type='submit' name='button'>Submit</button>
    </form>

    <div>
    <p> Response: </p> <br />
    {{ result ? result : 'waiting for response' }}
    </div>
  </div>

</template>

<script>
import axios from 'axios';

export default {
  name: 'formPost',
  data() {
    return {
      air_pressure: '',
      airport_elevation: '',
      outside_air_temp: '',
      runway_length_uncorrected: '',
      head_wind: '',
      slope_percent: '',
      aircraft_weight: '',
      ap_registration: '',
      air_conditioning: '',
      engine_anti_ice: '',
      total_anti_ice: '',
      operational_CG_percentage: '',
      show: false,
    };
  },
  methods: {
    postNow() {
      const form = new FormData();
      form.append('air_pressure', this.air_pressure);
      form.append('airport_elevation', this.airport_elevation);
      form.append('outside_air_temp', this.outside_air_temp);
      form.append('runway_length_uncorrected', this.runway_length_uncorrected);
      form.append('head_wind', this.head_wind);
      form.append('slope_percent', this.slope_percent);
      form.append('aircraft_weight', this.aircraft_weight);
      form.append('ap_registration', this.ap_registration);
      form.append('air_conditioning', this.air_conditioning);
      form.append('engine_anti_ice', this.engine_anti_ice);
      form.append('total_anti_ice', this.total_anti_ice);
      form.append('operational_CG_percentage', this.operational_CG_percentage);
      axios
        .post('https://8000-cdbd906f-55a3-48bb-aeac-f8d33e8d3537.ws-us02.gitpod.io/calculate', form, { errorHandle: false })
        .then((response) => {
          this.result = response.data;
          this.$forceUpdate();
        })
        .catch((error) => {
          this.errors = error.response.data.errors;
        });
    },
  },
};
</script>
