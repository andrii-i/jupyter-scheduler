import React, { ChangeEvent } from 'react';

import { FormLabel, Stack, TextField } from '@mui/material';

import { Cluster } from './components/cluster';
import { AddButton, DeleteButton } from './components/icon-buttons';
import { useTranslator } from './hooks';
import { JobsView } from './model';
import { Scheduler } from './tokens';
import { LabeledValue } from './components/labeled-value';

const AdvancedOptions = (
  props: Scheduler.IAdvancedOptionsProps
): JSX.Element => {
  const formPrefix = 'jp-create-job-advanced-';

  const trans = useTranslator('jupyterlab');

  // Check if this is a QASM file
  const isQasmFile = props.model.inputFile?.endsWith('.qasm');

  // Helper to get parameter value by name
  const getParamValue = (name: string): string => {
    const param = props.model.parameters?.find(p => p.name === name);
    return param?.value?.toString() ?? '';
  };

  // Helper to set parameter value by name
  const setParamValue = (name: string, value: string) => {
    if (props.jobsView !== JobsView.CreateForm) {
      return;
    }
    const params = [...(props.model.parameters ?? [])];
    const idx = params.findIndex(p => p.name === name);
    if (idx >= 0) {
      params[idx] = { name, value };
    } else {
      params.push({ name, value });
    }
    props.handleModelChange({
      ...props.model,
      parameters: params
    });
  };

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (props.jobsView !== JobsView.CreateForm) {
      return;
    }

    props.handleModelChange({
      ...props.model,
      [e.target.name]: e.target.value
    });
  };

  const handleTagChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (props.jobsView !== JobsView.CreateForm) {
      return;
    }

    const { name, value } = event.target;
    const tagIdxMatch = name.match(/^tag-(\d+)$/);

    if (tagIdxMatch === null) {
      return null;
    }

    const newTags = props.model.tags ?? [];
    newTags[parseInt(tagIdxMatch[1])] = value;

    props.handleModelChange({
      ...props.model,
      tags: newTags
    });
  };

  const addTag = () => {
    if (props.jobsView !== JobsView.CreateForm) {
      return;
    }

    const newTags = [...(props.model.tags ?? []), ''];
    props.handleModelChange({
      ...props.model,
      tags: newTags
    });
  };

  const deleteTag = (idx: number) => {
    if (props.jobsView !== JobsView.CreateForm) {
      return;
    }

    const newTags = props.model.tags ?? [];
    newTags.splice(idx, 1);
    props.handleModelChange({
      ...props.model,
      tags: newTags
    });
  };

  const tags = props.model.tags ?? [];

  const createTags = () => {
    return (
      <Stack spacing={2}>
        {tags.map((tag, idx) => (
          <Cluster key={idx} justifyContent="flex-start">
            <TextField
              label={trans.__('Tag %1', idx + 1)}
              id={`${formPrefix}tag-${idx}`}
              name={`tag-${idx}`}
              value={tag}
              onChange={handleTagChange}
            />
            <DeleteButton
              onClick={() => {
                // Remove tag
                deleteTag(idx);
                return false;
              }}
              title={trans.__('Delete tag %1', idx + 1)}
              addedStyle={{ marginTop: '4px' }}
            />
          </Cluster>
        ))}
        <Cluster justifyContent="flex-start">
          <AddButton
            onClick={(e: React.MouseEvent) => {
              addTag();
              return false;
            }}
            title={trans.__('Add new tag')}
          />
        </Cluster>
      </Stack>
    );
  };

  const showTags = () => {
    if (!props.model.tags) {
      return (
        <Stack spacing={2}>
          <p>
            <em>{trans.__('No tags')}</em>
          </p>
        </Stack>
      );
    }

    return (
      <Stack spacing={2}>
        {tags.map((tag, idx) => (
          <LabeledValue
            label={trans.__('Tag %1', idx + 1)}
            id={`${formPrefix}tag-${idx}`}
            name={`tag-${idx}`}
            value={tag}
          />
        ))}
      </Stack>
    );
  };

  // Tags look different when they're for display or for editing.
  const tagsDisplay: JSX.Element | null =
    props.jobsView === JobsView.CreateForm ? createTags() : showTags();

  // The idempotency token is only used for jobs, not for job definitions
  const idemTokenLabel = trans.__('Idempotency token');
  const idemTokenName = 'idempotencyToken';
  const idemTokenId = `${formPrefix}${idemTokenName}`;
  return (
    <Stack spacing={4}>
      {/* QASM-specific options */}
      {isQasmFile && props.jobsView === JobsView.CreateForm && (
        <>
          <FormLabel component="legend">
            {trans.__('QASM Execution Options')}
          </FormLabel>
          <TextField
            label={trans.__('Shots')}
            type="number"
            variant="outlined"
            value={getParamValue('shots') || '1000'}
            onChange={e => setParamValue('shots', e.target.value)}
            helperText={trans.__('Number of measurement samples')}
            id={`${formPrefix}shots`}
            name="shots"
            inputProps={{ min: 1 }}
          />
        </>
      )}
      {props.jobsView === JobsView.JobDetail && (
        <LabeledValue
          label={idemTokenLabel}
          value={props.model.idempotencyToken}
          id={`${formPrefix}idempotencyToken`}
          name={idemTokenName}
        />
      )}
      {props.jobsView === JobsView.CreateForm &&
        props.model.createType === 'Job' && (
          <TextField
            label={idemTokenLabel}
            variant="outlined"
            onChange={handleInputChange}
            value={props.model.idempotencyToken}
            id={idemTokenId}
            name={idemTokenName}
          />
        )}
      <FormLabel component="legend">{trans.__('Tags')}</FormLabel>
      {tagsDisplay}
    </Stack>
  );
};

export default AdvancedOptions;
