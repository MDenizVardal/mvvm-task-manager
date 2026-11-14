package com.example.amadlab

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.amadlab.ui.theme.AmadLabTheme

@Composable
fun TaskDetailRoute(
    onBack: () -> Unit,
    viewModel: TaskDetailViewModel = viewModel()   // a separate view model for every opened task
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    TaskDetailScreen(
        state = state,
        onBack = onBack,
        onTitleChange = viewModel::onTitleChange,
        onSave = {
            viewModel.save()
            onBack()                                 // task 3.3: return to the list (popBackStack)
        },
        onToggle = viewModel::toggle,
        onDelete = {
            viewModel.delete()
            onBack()
        }
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TaskDetailScreen(
    state: TaskDetailUiState,
    onBack: () -> Unit,
    onTitleChange: (String) -> Unit,
    onSave: () -> Unit,
    onToggle: () -> Unit,
    onDelete: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Task details") },
                navigationIcon = { TextButton(onClick = onBack) { Text("Back") } },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer
                )
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .padding(innerPadding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            val task = state.task
            if (task == null) {
                Text("This task does not exist any more.")
            } else {
                TaskDetailContent(task, state, onTitleChange, onSave, onToggle, onDelete)
            }
        }
    }
}

@Composable
private fun TaskDetailContent(
    task: Task,
    state: TaskDetailUiState,
    onTitleChange: (String) -> Unit,
    onSave: () -> Unit,
    onToggle: () -> Unit,
    onDelete: () -> Unit
) {
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Text(task.title, style = MaterialTheme.typography.headlineSmall)
        Text("Status: ${if (task.done) "done" else "to do"}")
        Text("id: ${task.id}", style = MaterialTheme.typography.bodySmall)

        // Task 3.3: editing of the title
        OutlinedTextField(
            value = state.editedTitle,
            onValueChange = onTitleChange,
            label = { Text("Title") },
            singleLine = true,
            modifier = Modifier.fillMaxWidth()
        )
        Button(onClick = onSave, enabled = state.canSave, modifier = Modifier.fillMaxWidth()) {
            Text("Save")
        }
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = onToggle) {
                Text(if (task.done) "Mark as not done" else "Mark as done")
            }
            OutlinedButton(onClick = onDelete) { Text("Delete") }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun TaskDetailScreenPreview() {
    AmadLabTheme {
        TaskDetailScreen(
            state = TaskDetailUiState(Task(3, "Read about MVVM"), "Read about MVVM and UDF"),
            onBack = {}, onTitleChange = {}, onSave = {}, onToggle = {}, onDelete = {}
        )
    }
}
