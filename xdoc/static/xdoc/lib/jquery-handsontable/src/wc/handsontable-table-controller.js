function parseDatacolumn(HOTCOLUMN) {
  var obj = {};

  for (var i = 0, ilen = HOTCOLUMN.attributes.length; i < ilen; i++) {
    obj[HOTCOLUMN.attributes[i].name] = HOTCOLUMN.attributes[i].value || true;
  }

  obj.data = obj.value;
  delete obj.value;

  obj.readOnly = obj.readonly;
  delete obj.readonly;

  obj.strict = readBool(obj.strict);

  obj.checkedTemplate = obj.checkedtemplate;
  delete obj.checkedtemplate;

  obj.uncheckedTemplate = obj.uncheckedtemplate;
  delete obj.uncheckedtemplate;

  if (obj.type === 'autocomplete' && typeof obj.source === 'string') {
    obj.source = window[obj.source];
  }

  var HANDSONTABLE = HOTCOLUMN.getElementsByTagName('handsontable-table');
  if (HANDSONTABLE.length) {
    obj.handsontable = parseHandsontable(HANDSONTABLE[0]);
  }

  return obj;
}

function getModel(HANDSONTABLE) {
  if (HANDSONTABLE.templateInstance) {
    return HANDSONTABLE.templateInstance.model;
  }
  else {
    return window;
  }
}

function getModelPath(HANDSONTABLE, path) {
  var obj = getModel(HANDSONTABLE);
  var keys = path.split('.');
  var len = keys.length;
  for (var i = 0; i < len; i++) {
    if (obj[keys[i]]) {
      obj = obj[keys[i]];
    }
  }
  return obj;
}

function parseDatacolumns(HANDSONTABLE) {
  var columns = []
    , i
    , ilen;

  for (i = 0, ilen = HANDSONTABLE.childNodes.length; i < ilen; i++) {
    if (HANDSONTABLE.childNodes[i].nodeName === 'HANDSONTABLE-COLUMN') {
      columns.push(parseDatacolumn(HANDSONTABLE.childNodes[i]));
    }
  }

  return columns;
}

function parseHandsontable(HANDSONTABLE) {
  var i;
  var columns = parseDatacolumns(HANDSONTABLE);

  var options = {
  };

  if (columns.length) {
    options.columns = columns;
  }

  return options;
}

var publicMethods = ['updateSettings', 'loadData', 'render', 'setDataAtCell', 'setDataAtRowProp', 'getDataAtCell', 'getDataAtRowProp', 'countRows', 'countCols', 'rowOffset', 'colOffset', 'countVisibleRows', 'countVisibleCols', 'clear', 'clearUndo', 'getData', 'alter', 'getCell', 'getCellMeta', 'selectCell', 'deselectCell', 'getSelected', 'destroyEditor', 'getRowHeader', 'getColHeader', 'destroy', 'isUndoAvailable', 'isRedoAvailable', 'undo', 'redo', 'countEmptyRows', 'countEmptyCols', 'isEmptyRow', 'isEmptyCol', 'parseSettingsFromDOM', 'addHook', 'addHookOnce', 'getValue', 'getInstance', 'getSettings'];
var publicProperties = Object.keys(Handsontable.DefaultSettings.prototype);
publicProperties.push('settings');

var publish = {
};

publicMethods.forEach(function (hot_method) {
  publish[hot_method] = function () {
    return this.instance[hot_method].apply(this.instance, arguments);
  }
});

publicProperties.forEach(function (hot_prop) {
  if (!publish[hot_prop]) {
    var wc_prop = hot_prop;

    if (hot_prop === 'data') {
      wc_prop = 'datarows';
    }

    if (Handsontable.DefaultSettings.prototype[hot_prop] === void 0) {
      publish[wc_prop] = null; //Polymer does not like undefined
    }
    else if (hot_prop === 'observeChanges') {
      publish[wc_prop] = true; //on by default
    }
    else {
      publish[wc_prop] = Handsontable.DefaultSettings.prototype[hot_prop];
    }

    publish[wc_prop + 'Changed'] = function () {
      if(wc_prop === 'settings') {
        var settings = getModelPath(this, this[wc_prop]);
        this.updateSettings(settings);
        return;
      }

      var update = {};
      if (wc_prop === 'datarows') {
        update[hot_prop] = getModelPath(this, this[wc_prop])
      }
      else if (typeof Handsontable.DefaultSettings.prototype[hot_prop] === 'boolean') {
        update[hot_prop] = readBool(this[wc_prop]);
      }
      else {
        update[hot_prop] = this[wc_prop];
      }
      this.updateSettings(update);
    }
  }
});

function readBool(val) {
  if (val === void 0 || val === "false") {
    return false;
  }
  return val;
}

Polymer('handsontable-table', {
  instance: null,
  enteredView: function () {
    this.shadowRoot.applyAuthorStyles = true; //only way I know to let override Shadow DOM styles (just define ".handsontable td" in page stylesheet)
    jQuery(this.$.htContainer).handsontable(parseHandsontable(this));
    this.instance = jQuery(this.$.htContainer).data('handsontable');
  },
  onMutation: function() {
    var columns = parseDatacolumns(this);
    if (columns.length) {
      this.updateSettings({columns: columns});
    }
  },
  publish: publish
});