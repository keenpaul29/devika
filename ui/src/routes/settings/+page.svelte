<script>
  import { updateSettings, fetchSettings, fetchInitialData } from "$lib/api";
  import { onMount } from "svelte";
  import { modelList, searchEngineList, selectedModel, selectedSearchEngine } from "$lib/store";
  import * as Tabs from "$lib/components/ui/tabs";
  import { setMode } from "mode-watcher";
  import * as Select from "$lib/components/ui/select/index.js";
  import Seperator from "../../lib/components/ui/Seperator.svelte";
  import { toast } from "svelte-sonner";

  let settings = {};
  let editMode = false;
  let original = {};

  function getSelectedTheme() {
    let theme = localStorage.getItem('mode-watcher-mode');
    if (theme === "light") {
      return { value: "light", label: "Light" };
    } else if (theme === "dark") {
      return { value: "dark", label: "Dark" };
    } else if (theme === "system") {
      return { value: "system", label: "System" };
    } else {
      return { value: "system", label: "System" };
    }
  }

  function getSelectedResize() {
    let resize = localStorage.getItem('resize');
    if (resize === "enable") {
      return { value: "enable", label: "Enable" };
    } else {
      return { value: "disable", label: "Disable" };
    }
  }

  let selectedTheme = getSelectedTheme();
  let selectedResize = getSelectedResize();

  function setResize(value) {
    localStorage.setItem('resize', value);
  }

  onMount(async () => {
    await fetchInitialData();
    settings = await fetchSettings();
    settings["API_KEYS"] = {
      "BING": settings["API_KEYS"]["BING"],
      "GOOGLE_SEARCH": settings["API_KEYS"]["GOOGLE_SEARCH"],
      "GOOGLE_SEARCH_ENGINE_ID": settings["API_KEYS"]["GOOGLE_SEARCH_ENGINE_ID"],
      "CLAUDE": settings["API_KEYS"]["CLAUDE"],
      "OPENAI": settings["API_KEYS"]["OPENAI"],
      "GEMINI": settings["API_KEYS"]["GEMINI"],
      "MISTRAL": settings["API_KEYS"]["MISTRAL"],
      "GROQ": settings["API_KEYS"]["GROQ"],
      "NETLIFY": settings["API_KEYS"]["NETLIFY"]
    };
    original = JSON.parse(JSON.stringify(settings));
  });

  const save = async () => {
    let updated = {};
    for (let key in settings) {
      for (let subkey in settings[key]) {
        if (settings[key][subkey] !== original[key][subkey]) {
          if (!updated[key]) {
            updated[key] = {};
          }
          updated[key][subkey] = settings[key][subkey];
        }
      }
    }

    await updateSettings(updated);
    editMode = !editMode;
  };

  const edit = () => {
    editMode = !editMode;
  };
</script>

<div class="p-4 h-full w-full gap-8 flex flex-col overflow-y-auto">
  <h1 class="text-3xl">Settings</h1>
  <div class="flex flex-col w-full text-sm">
    <Tabs.Root value="apikeys" class="w-full flex flex-col justify-start ms-2">
      <Tabs.List class="ps-0">
        <Tabs.Trigger value="apikeys">API Keys</Tabs.Trigger>
        <Tabs.Trigger value="endpoints">API Endpoints</Tabs.Trigger>
        <Tabs.Trigger value="config">Config</Tabs.Trigger>
        <Tabs.Trigger value="appearance">Appearance</Tabs.Trigger>
        <Tabs.Trigger value="model">Model</Tabs.Trigger>
        <Tabs.Trigger value="search">Search Engine</Tabs.Trigger>
      </Tabs.List>
      
      <Seperator direction="vertical"/>
      
      <Tabs.Content value="apikeys" class="mt-4">
        {#if settings["API_KEYS"]}
          <div class="flex gap-4 w-full">
            <div class="flex flex-col gap-4 w-full">
              <div class="flex flex-col gap-4">
                {#each Object.entries(settings["API_KEYS"]) as [key, value]}
                  <div class="flex gap-1 items-center">
                    <p class="w-48">{key.toLowerCase()}</p>
                    <input
                      type={editMode ? "text" : "password"}
                      value={settings["API_KEYS"][key]}
                      on:input={(e) => settings["API_KEYS"][key] = e.target.value}
                      name={key}
                      class="p-2 border-2 w-1/2 rounded-lg {editMode ? '' : ' text-gray-500'}"
                      readonly={!editMode}
                    />
                  </div>
                {/each}
              </div>
            </div>
          </div>
        {/if}
        <div class="flex gap-4 mt-5">
          {#if !editMode}
            <button
              id="btn-edit"
              class="p-2 border-2 rounded-lg flex gap-3 items-center hover:bg-secondary"
              on:click={edit}
            >
              <i class="fas fa-edit"></i>
              Edit
            </button>
          {:else}
            <button
              id="btn-save"
              class="p-2 border-2 rounded-lg flex gap-3 items-center hover:bg-secondary"
              on:click={save}
            >
              <i class="fas fa-save"></i>
              Save
            </button>
          {/if}
        </div>
      </Tabs.Content>

      <!-- Other Tabs.Content sections remain unchanged -->

      <Tabs.Content value="model" class="mt-4">
        <div class="flex flex-col gap-4">
          <div class="text-xl font-semibold">Select Model</div>
          {#if $modelList}
            <Select.Root onSelectedChange={(v) => selectedModel.set(v.value)}>
              <Select.Trigger class="w-[180px]">
                <Select.Value placeholder={$selectedModel || "Select model"} />
              </Select.Trigger>
              <Select.Content>
                <Select.Group>
                  {#each Object.entries($modelList) as [key, value]}
                    <Select.Item value={key} label={value}>{value}</Select.Item>
                  {/each}
                </Select.Group>
              </Select.Content>
            </Select.Root>
          {/if}
        </div>
      </Tabs.Content>

      <Tabs.Content value="search" class="mt-4">
        <div class="flex flex-col gap-4">
          <div class="text-xl font-semibold">Select Search Engine</div>
          {#if $searchEngineList}
            <Select.Root onSelectedChange={(v) => selectedSearchEngine.set(v.value)}>
              <Select.Trigger class="w-[180px]">
                <Select.Value placeholder={$selectedSearchEngine || "Select search engine"} />
              </Select.Trigger>
              <Select.Content>
                <Select.Group>
                  {#each $searchEngineList as engine}
                    <Select.Item value={engine} label={engine}>{engine}</Select.Item>
                  {/each}
                </Select.Group>
              </Select.Content>
            </Select.Root>
          {/if}
        </div>
      </Tabs.Content>
    </Tabs.Root>
  </div>
</div>
