<script>
    import {onMount} from 'svelte';
    import {Splide, SplideSlide} from '@splidejs/svelte-splide';
    import TestGeneralForm from './forms/TestGeneralForm.svelte';
    import TestQuestionsForm from './forms/TestQuestionsForm.svelte';
    import TestResultsForm from './forms/TestResultsForm.svelte';
    import TestSubmitForm from './forms/TestSubmitForm.svelte';
    import SplideControls from '../components/SplideControls.svelte';
    import '@splidejs/splide/dist/css/splide.min.css';

    import {general, questions, results} from './default-test-values';

    let splide;
    let test;

    const options = {
        perPage: 1,
        gap: '10px',
        perMove: 1,
        arrows: false,
        pagination: false,
        keyboard: false,
        drag: false,
        wheel: false,
        width: '100%',
        waitForTransition: false,
    };

    const slides = [
      'Основное',
      'Вопросы',
      'Результаты',
      'Сохранить',
    ];

    const getTest = () => {
        test = {
            general,
            questions,
            results,
        };
        console.log(test);
    };

    onMount(getTest);
</script>
<div class="slider">
  {#if test}
    <SplideControls {slides} {splide}/>
    <Splide {options} bind:this={ splide }>
      <SplideSlide>
        <TestGeneralForm bind:data={test.general}/>
      </SplideSlide>
      <SplideSlide>
        <TestQuestionsForm bind:questions={test.questions}/>
      </SplideSlide>
      <SplideSlide>
        <TestResultsForm bind:results={test.results}/>
      </SplideSlide>
      <SplideSlide>
        <TestSubmitForm bind:test/>
      </SplideSlide>
    </Splide>
  {:else}
    Loading...
  {/if}
  <pre>
      {JSON.stringify(test, null, 2)}
    </pre>

</div>


<style>
    .slider {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
</style>