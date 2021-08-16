<script>
  import Login from "./Panels/Login.svelte";
  import { authenticated } from "./store.js";
  $: console.log($authenticated);
</script>

{#if $authenticated}
  Hello
{:else}
  <Login />
{/if}
